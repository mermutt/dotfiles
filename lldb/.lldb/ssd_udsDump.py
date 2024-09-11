import sys
import lldb
import optparse
import shlex
import re
import lldbutils

# to enable printing processing time for each high level variable uncomment
# 3 places: here and other two where teatime is mentioned
#from time import time
#teatime = 0

MAX_NUMBER_OF_CHARACTERS_IN_ONE_LINE = 150

threat = 0
pointerSize = 4
debug = False

oneLineVars = []
specialHandlingString = ''
rowStartIndex = 0
rowEndIndex = 0
lineNumber = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
lastPrintedLevel = 0
CursorColumn = 0
reentrancyLevel = 0
CompoundName = ''

target = 0

# Controls of foldings of large arrays. By default all large arrays are being folded.
# Making it 1 will disable of foldings of top level arrays. Useful for interactive mode
# to enable printing large arrays when user specifically asked for it.
TopLevelArrayFoldingDisable = 0

def enum(*args):
   enums = dict(zip(args, range(len(args))))
   return type('Enum', (), enums)

RecTypes = enum( 'Base', 'Struct', 'Array', 'Pointer', 'BitField', 'String' )

def WalkLinksAtSentinel( start, link_type, function = None ):
   global target
   '''
   This function takes two arguments
   start is address of stx link sentinel to start walking from
   link_type is either stx_single_link_sentinel or stx_double_link
   function is optional parameter. function() will be called for each element
   '''
   Sentinel = target.FindFirstType( link_type )

   link_type += '*'

   loop = 0
   filtered_matches = 0
   ptr_next = int( start, 0 )
   if ptr_next == 0:
      return 0

   sb_addr = lldb.SBAddress( ptr_next, target )
   Sentinel_ptr = target.CreateValueFromAddress( link_type, sb_addr, Sentinel )
   ptr_previous = Sentinel_ptr.GetChildMemberWithName( "Previous" ).GetValueAsUnsigned( )
   ptr_next = Sentinel_ptr.GetChildMemberWithName( "Next" ).GetValueAsUnsigned( )

   while True:
      next_addr = lldb.SBAddress( ptr_next, target )
      if ptr_next == 0:
         break
      if function:
         if function( ptr_next ):
            filtered_matches += 1
      Sentinel_ptr = target.CreateValueFromAddress( link_type, next_addr, Sentinel )
      ptr_next = Sentinel_ptr.GetChildMemberWithName( "Next" ).GetValueAsUnsigned( )

      loop += 1
      # Bail out at large value.
      if ( loop >= 10000 ):
         break
      if ptr_next == ptr_previous:
         break

   if function:
      return filtered_matches
   else:
      return loop

def stxDoubleLinkSentinel( var ):
   global oneLineVars
   found = WalkLinksAtSentinel( var.GetChildMemberWithName( 'Next' ).AddressOf( ).GetValue(), 'stx_double_link' )
   string = '%s {%s=%s, %s=%s} // %s has %d entries' % ( var.name, var.GetChildAtIndex( 0 ).name, var.GetChildAtIndex( 0 ).value, var.GetChildAtIndex( 1 ).name, var.GetChildAtIndex( 1 ).value, var.GetTypeName(), found )
   oneLineVars.append( ( var, RecTypes.String, reentrancyLevel, 0, string ) )
   return False

def ssdMemRequestType( var ):
   global reentrancyLevel

   reqType = var.GetChildMemberWithName( 'CommonData' ).GetChildMemberWithName( 'Flags' ).GetChildMemberWithName( 'Field' ).GetChildMemberWithName( 'Type').GetValueAsUnsigned( )
   if reqType == 0:
      localVar = var.GetChildMemberWithName( 'Xor' )
   elif reqType == 1:
      localVar = var.GetChildMemberWithName( 'Compare' )
   elif reqType == 2:
      localVar = var.GetChildMemberWithName( 'Copy' )
   reentrancyLevel -= 1
   genericVarPrint( localVar, RecTypes.Base, 0, 0 )
   reentrancyLevel += 1
   return False

def stxSingleLinkSentinel( var ):
   global oneLineVars
   found = WalkLinksAtSentinel( var.GetChildAtIndex( 0 ).AddressOf( ).GetValue(), 'stx_single_link' )
   string = '%s {%s=%s, %s=%s} \t\t// %s has %d entries' % ( var.name, var.GetChildAtIndex( 0 ).name, var.GetChildAtIndex( 0 ).value, var.GetChildAtIndex( 1 ).name, var.GetChildAtIndex( 1 ).value, var.GetTypeName(), found )
   oneLineVars.append( ( var, RecTypes.String, reentrancyLevel, 0, string ) )
   return False

def shv_UsedRequestSentinel_Function( link_addr ):
   global specialHandlingString, target
   stateMachine = target.FindFirstType( "quality_readErrorRecovery_stateMachine" )
   sb_addr = lldb.SBAddress( link_addr, target )
   sm_ptr = target.CreateValueFromAddress( "quality_readErrorRecovery_stateMachine", sb_addr, stateMachine )
   specialHandlingString += sm_ptr.GetChildMemberWithName( "Index" ).GetValue( ) + ", "
   return True

def shv_UsedRequestSentinel( var ):
   global oneLineVars, specialHandlingString
   specialHandlingString = ""
   found = WalkLinksAtSentinel( var.GetChildAtIndex( 0 ).AddressOf( ).GetValue(), 'stx_single_link', shv_UsedRequestSentinel_Function )
   string = '%s {%s=%s, %s=%s} // %d state machines: %s' % ( var.name, var.GetChildAtIndex( 0 ).name, var.GetChildAtIndex( 0 ).value, var.GetChildAtIndex( 1 ).name, var.GetChildAtIndex( 1 ).value, found, specialHandlingString )
   oneLineVars.append( ( var, RecTypes.String, reentrancyLevel, 0, string ) )
   return False

global_exclude_list = [ 'pDLL', 'global_state', 'TestRandState', 'helpString', 'interfaceHelpString', 'mediaContHelpString', 'virtHelpString' ]
special_handling_variables = { 'UsedRequestSentinel' : shv_UsedRequestSentinel, 'PausedRequestSentinel' : shv_UsedRequestSentinel, 'MissingDcwRequestSentinel' : shv_UsedRequestSentinel, 'Sentinel' : stxDoubleLinkSentinel }
special_handling_types = { 'stx_single_link_sentinel' : stxSingleLinkSentinel, 'ssd_mem_request' : ssdMemRequestType }

def isHandlingRequired( CompoundName, var ):
   #if CompoundName[1:] in special_handling_variables:
      #return special_handling_variables[ CompoundName[1:] ]( var )
   if var.name in special_handling_variables:
      return special_handling_variables[ var.name ]( var )
   elif var.GetTypeName() in special_handling_types:
      return special_handling_types[var.GetTypeName()]( var )
   return True


def memPrint( startAddr, length ):
   mem_read_string = ( "memory read -s1 -l32 -fx -c0x%x --force " % length ) + startAddr
   lldb.debugger.HandleCommand( mem_read_string )

# I left it here for reference. I used this func to call memcmp on targets memory. I found
# it is getting slower and slower after thousands of calls. Now I use process.ReadMemory
# and data comparison in Python instead. Works faster.
# From: http://stackoverflow.com/questions/38138060/using-lldb-commands-in-python-script
def command_function( addrA, addrB, size ):
   global thread

   if thread.IsValid( ):
      frame = thread.GetSelectedFrame( )
      expr_str = '(int)memcmp(' + addrA + ',' + addrB + ',' + size + ')'
      value = frame.EvaluateExpression( expr_str )
      #value = frame.EvaluateExpression( expr_str, lldb.eNoDynamicValues )
      #value = frame.EvaluateExpression( expr_str, lldb.eDynamicCanRunTarget )
      if value.GetError().Success( ):
         return int( value.value )
   return 0

def fast_array_elements_comparison( var, idxA ):
   '''
   Compares array elements to each other and returns number of matches. Example:
   var is array of [50] entries and idxA = 0 (start from beginning). Then this func
   will compare v[0] to v[1] if no match it would return 0
   if match then it would compare v[0-1] to v[2-3] if no match it would return 1
   if match then it would compare v[0-3] to v[4-7] if no match it would return 3
   etc.
   It would multiply the range by 2 always until the end of the array. This approach allows
   for quick comparisons even on hughe arrays.
   '''

   # From: http://stackoverflow.com/questions/38138060/using-lldb-commands-in-python-script
   def compare_memory( addrA, addrB, size ):
      global thread
   
      process = thread.process
      error = lldb.SBError()

      bytesA = process.ReadMemory( addrA, size, error )
      if error.Success( ):
         bytesB = process.ReadMemory( addrB, size, error )
         if error.Success( ):
             if bytesA == bytesB:
                 return 0
      return 1

   step = 1
   addrA = var.GetChildAtIndex( idxA ).AddressOf( ).GetValueAsUnsigned( )
   addrB = var.GetChildAtIndex( idxA + step ).AddressOf( ).GetValueAsUnsigned( )
   size = addrB - addrA
   lastVar = var.GetChildAtIndex( var.GetNumChildren() - 1 )
   addrZ = lastVar.AddressOf( ).GetValueAsUnsigned() + int( lastVar.size )
   retValue = 0

   if addrA != 0 and addrB != 0:
       while addrB + size <= addrZ:
          if compare_memory( addrA, addrB, size ):
             break
          retValue += step
          addrB += size
          size *= 2
          step *= 2
   return retValue

def genericVarPrint( var, varType, arrayIndex, Size ):
   global oneLineVars, reentrancyLevel, CompoundName, rowStartIndex, rowEndIndex, lineNumber, lastPrintedLevel, CursorColumn, debug

   def roll_back_records_and_update( index ):
      global oneLineVars, reentrancyLevel

      rollBackList = []
      while len( oneLineVars ):
         prevRecord = oneLineVars.pop( )
         if prevRecord[2] == reentrancyLevel + 1:
            break
         rollBackList.append( prevRecord )
      oneLineVars.append( ( prevRecord[0],  prevRecord[1], prevRecord[2], prevRecord[3] , index - 1 ) )
      for i in range( 0, len( rollBackList ) ):
         oneLineVars.append( rollBackList.pop( ) )

   def get_reentrancy_string( level ):
      string = ' '
      for index in range( 1, level ):
          string += '   '
      return string

   def flush_accumulated_info( ):
      global oneLineVars, lastPrintedLevel, CursorColumn, debug, target

      def get_string_value( var, vType, bitFieldSize, lastRepeatingIdx ):
         global debug

         if debug:
            print '>>>', var.name, vType,
         if vType == RecTypes.Pointer:
            string = '%s ->(%s) ' % ( var.name, var.Dereference( ).GetTypeName() )
            # There was a case when var.value was None for local pointer.
            if not var.value:
               string += 'Unknown'
            elif int( var.value, 0 ) == 0:
               string += 'NULL'
            else:
               string += '@%s' % ( var.value )
         elif vType == RecTypes.Array:
            string = ''
            if var.GetNumChildren( ) and not var.TypeIsPointerType( ):
               string += '= {'
            elif lastRepeatingIdx:
               string += '('
            if var.value:
               # Workaround for uint32_t. It gets printed as decimal despite this record "type format add -f hex uint32_t" in .lldbinit 
               # Same records for other types like uint16_t and uint64_t gets printed fine by else: clause (as strings)
               if var.GetTypeName( ) == 'uint32_t':
                  string += '{value:#010x}'.format( value=int( var.value, 0 ) )
               else:
                  string += '%s' % var.value
            if lastRepeatingIdx and ( not var.GetNumChildren( ) or var.TypeIsPointerType( ) ):
               string += ')'
         else:
            string = '%s = ' % var.name
            if var.value:
               if vType == RecTypes.BitField:
                  try:
                     value = int( var.value, 0 )
                     if bitFieldSize > 3:
                        string += '{value:#0{width}x}'.format( value=value, width = 2 + ( bitFieldSize + 3 ) / 4 )
                     else:
                        string += '{value:{width}}'.format( value=value, width=1)
                  except:
                     string += '%s' % var.value
               else:

                   # Workaround for uint32_t. It gets printed as decimal despite this record "type format add -f hex uint32_t" in .lldbinit 
                   # Same records for other types like uint16_t and uint64_t gets printed fine by else: clause (as strings)
                  if var.GetTypeName( ) == 'uint32_t':
                     string += '{value:#010x}'.format( value=int( var.value, 0 ) )
                  else:
                     string += '%s' % var.value

            elif var.GetNumChildren():
               string += '{'
            else:
               string += 'Unknown'

         # If var is a pointer and is not a complex type (do not have children), try to match it to symbol.
         # this adds function names to function pointers.
         if var.TypeIsPointerType( ) and not var.GetNumChildren( ):
            tempString = target.ResolveLoadAddress( var.GetValueAsUnsigned( ) )
            if tempString.GetFunction( ):
               string += " (" + tempString.GetFunction( ).name + ")"

         if debug:
            print  var.value, bitFieldSize, lastRepeatingIdx, '=>', string, len( string ), '<<<'
         return string

      def can_fit_in_current_line( var, numToFit ):
         global oneLineVars, CursorColumn, pointerSize, TopLevelArrayFoldingDisable
         
         #if var[0].name == 'BxorReqTransmitterAop1':
         #   debug = True
         #debug = True

         string_len = CursorColumn + len( get_string_value( var[0], var[1], var[3], var[4] ) )
         level = var[2]

         if debug:
            print '^^^', CursorColumn, var[0].name, string_len, level

         for i in range( 0, len( oneLineVars ) ):
            # Strings always can fit because they are special cases and code printing them would take care of new lines.
            if oneLineVars[i][1] == RecTypes.String:
               if debug:
                  print '*tS', oneLineVars[i][0].name,
               return True
            # If we processed number of elements we were to fit then return True to say Yes, can fit
            if i >= numToFit:
               if debug:
                  print '*tNum', oneLineVars[i][0].name, i 
               return True
            if level > oneLineVars[i][2]:
               if debug:
                  print '*t', string_len, oneLineVars[i][0].name,
               return True
            if debug:
               print '[[', i, oneLineVars[i][0].name, oneLineVars[i][0].value, oneLineVars[i][1], oneLineVars[i][3],
            string_len += len( get_string_value( oneLineVars[i][0], oneLineVars[i][1], oneLineVars[i][3], oneLineVars[i][4] ) ) + 2
            # cases where -%d is added to [%d<here>] are not counted by func above. So add it below
            if oneLineVars[i][4]:
               string_len += len( str( oneLineVars[i][4] ) ) + 1
            # Array names are not counted by the func above too. Add here.
            if oneLineVars[i][1] == RecTypes.Array and oneLineVars[i][0].GetNumChildren( ):
               string_len += len( str( oneLineVars[i][0].name ) )
            if debug:
               print string_len, ']]'
            if string_len > MAX_NUMBER_OF_CHARACTERS_IN_ONE_LINE:
               if debug:
                  print '*f', string_len, oneLineVars[i][0].name,
               return False
         if debug:
            print '*T', string_len,
         return True

      #print '%.2f' % ( time( ) - teatime )

      #if oneLineVars[0][0].name == 'SharedTcmAop0':
      #   debug = True
      if debug:
         print '+++', lastPrintedLevel, lineNumber[lastPrintedLevel]
         for ll in oneLineVars:
            print ll[0].name, ll[1], ll[2], ll[3], ll[4]
         print '---'

      while oneLineVars:
         rec = oneLineVars.pop( 0 )
         var, varType, varLevel, varSize, lastRepeatingIdx = rec
         string = ''

         if debug:
            print '\n(', lastPrintedLevel, lineNumber[lastPrintedLevel], CursorColumn, can_fit_in_current_line( rec, 1000 ), '>', var.name, varLevel, varSize, lastRepeatingIdx, ')'

         if lastPrintedLevel > varLevel:
            for level in range( lastPrintedLevel, varLevel, -1 ):
               if lineNumber[level]:
                  print '\n{: <{width}}'.format( '', width=pointerSize*2-1+(level-1)*3 ),
                  CursorColumn = 0
               print '}',
            lastPrintedLevel = varLevel
         elif lastPrintedLevel < varLevel:
            lastPrintedLevel = varLevel
            lineNumber[lastPrintedLevel] = 0

         if varType == RecTypes.String:
            string = '\n{addr:#0{width}x}'.format( addr=var.AddressOf( ).GetValueAsUnsigned(), width=pointerSize*2+2 ) + get_reentrancy_string( varLevel )
            print '%s%s' % ( string, lastRepeatingIdx ),

         # Processing array elements here. if a struct has lastRepeatingIdx then this struct is an element of an array
         elif varType == RecTypes.Array or lastRepeatingIdx:
            index = re.search('\[(\d+)\]', var.name )
            simpleElements = index and not var.GetNumChildren( )

            if varLevel == 1 or ( simpleElements and not can_fit_in_current_line( rec, 1 ) ) or ( not simpleElements and ( lineNumber[lastPrintedLevel] or not can_fit_in_current_line( rec, 1000 )  ) ):
               string = '\n{addr:#0{width}x}'.format( addr=var.AddressOf( ).GetValueAsUnsigned(), width=pointerSize*2+2 ) + get_reentrancy_string( varLevel )
               lineNumber[lastPrintedLevel] += 1
               CursorColumn = 0
               NewLineStarted = True
            else:
               NewLineStarted = False
            if index:
               if lastRepeatingIdx:
                  string += '[%d-%s] ' % ( int( index.group(1) ), str( lastRepeatingIdx ) )
               elif NewLineStarted or int( index.group(1) ) == 0:
                  string += var.name + ' '
            else:
               string += var.name + ' '
            string += get_string_value( var, RecTypes.Array, varSize, lastRepeatingIdx )
            print string,
            CursorColumn += len( string ) + 1
         else:
            if varLevel == 1 or lineNumber[lastPrintedLevel] or not can_fit_in_current_line( rec, 1000 ):
               string = '\n{addr:#0{width}x}'.format( addr=var.AddressOf( ).GetValueAsUnsigned(), width=pointerSize*2+2 ) + get_reentrancy_string( varLevel )
               lineNumber[lastPrintedLevel] += 1
               CursorColumn = 0
            string += get_string_value( var, varType, varSize, 0 )
            if oneLineVars and oneLineVars[0][2] == varLevel and not lineNumber[lastPrintedLevel]:
               string += ','
            print string,
            CursorColumn += len( string ) + 1
         lastPrintedLevel = varLevel
      if debug:
         print "===",


   #if not reentrancyLevel:
   #   teatime = time( )
   #   print '\n-------> Starting with -->', var.name,

   reentrancyLevel += 1

   if var.name not in global_exclude_list:
      # anonymous unions will have var.name == None
      if var.name:
         VarNameIndex = re.search('\[(\d+)\]', var.name )
      if var.name and VarNameIndex:
         CompoundName +=  '.[]'
      else:
         CompoundName +=  '.' + str( var.name )

      if isHandlingRequired( CompoundName, var ):
         if varType != RecTypes.BitField:
            # The following block would assign Size upon entry to an array.
            # It would not change Size for any member of array
            # it would clear Size for anything else except RecTypes.BitField
            # This works out for arrays of structures. Structure elements are not treated like array elements.
            TypeNameIndex = re.search('\[(\d+)\]', var.GetTypeName() )
            if TypeNameIndex and int( TypeNameIndex.group(1) ) == var.GetNumChildren( ):
               Size = var.GetNumChildren( )
            else:
               if var.name and not VarNameIndex:
                  Size = 0

         #if var.name and var.name == 'goldenData':
         #   debug = True
         if debug:
            if var.name:
               print 'var.name', var.name
            else:
               print 'noname', var.value
            print '\n%s @0x%08x [%d/%d] ptr?:%s' % ( var.name, var.AddressOf( ).GetValueAsUnsigned( ), var.GetNumChildren( ), Size, var.TypeIsPointerType( ) )

         # Check if var is complex type, like array, struct etc
         if var.GetNumChildren( ):
            if var.TypeIsPointerType( ):
               oneLineVars.append( ( var, RecTypes.Pointer, reentrancyLevel, 0, 0 ) )
            else:
               child = 0
               equalElementsComparison = False
               numSameChildren = 0

               # Check if current element is ordinary array element. It's name is [0] or [1134] etc
               # The array element maybe complex, e.g contain structs inside, still can be compared to equals
               childArray = re.search('\[(\d+)\]', var.GetChildAtIndex(0).name )
               if childArray:
                  # We are on array element, let's enable comparison with equals
                  equalElementsComparison = True
                  varType = RecTypes.Array
               else:
                  varType = RecTypes.Struct

               oneLineVars.append( ( var, varType, reentrancyLevel, Size, 0 ) )

               while child < var.GetNumChildren():
                  if equalElementsComparison:
                     if child and var.GetNumChildren() >= ( child + 1 ):
                        ret = fast_array_elements_comparison( var, child - 1 )
                        if ret:
                           child += ret
                           numSameChildren += ret
                           continue
                     # Do we have identical adjacent array elements?
                     if numSameChildren:
                        # See if we can 'fold' identical array elements. For simple types
                        # number of equals must be at least 16. 'Folding' complex types can be done even for 1 match.
                        if var.GetChildAtIndex(0).GetNumChildren( ) or numSameChildren > 3:
                           roll_back_records_and_update( child )
                           numSameChildren = 0
                        else:
                           # Number of equals is too low to 'fold'. Need to roll back and process them again
                           # so they will not be missing but be added to the oneLineVars. For that disable comparison
                           # temporarily and throw child index back.
                           equalElementsComparison = False
                           child -= numSameChildren
                  # comparison is disabled but numSameChildren indicates some matches found. We must be in 'unwind'
                  # back some elements.
                  elif numSameChildren:
                     numSameChildren -= 1
                     # all matching elements have been added to oneLineVars, lets re-enable matching comparison.
                     if not numSameChildren:
                        equalElementsComparison = True

                  if var.GetType( ).GetFieldAtIndex( child ).IsBitfield( ):
                     genericVarPrint( var.GetChildAtIndex( child ), RecTypes.BitField, child, var.GetType( ).GetFieldAtIndex( child).GetBitfieldSizeInBits( ) )
                  else:
                     genericVarPrint( var.GetChildAtIndex( child ), varType, child, Size )
                  child += 1
                  # if number of non same elements (same would have been folded before coming here) in array is larger than threshold it is too long to display here.
                  if childArray and child >= 100 and reentrancyLevel > TopLevelArrayFoldingDisable:
                     while True:
                        prevRecord = oneLineVars.pop( )
                        if prevRecord[2] == reentrancyLevel:
                           break
                     string = '%s { %s } \t\t// FOLDED' % ( var.name, var.GetTypeName() )
                     oneLineVars.append( ( var, RecTypes.String, reentrancyLevel, 0, string ) )
                     child = var.GetNumChildren( )
               if numSameChildren:
                  roll_back_records_and_update( child )
         else:
            oneLineVars.append( ( var, varType, reentrancyLevel, Size, 0 ) )

      CompoundName = CompoundName[:CompoundName.rfind( '.' )]

   # Flush if returning from processing a top level symbol
   if reentrancyLevel == 1:
      flush_accumulated_info( )
      for level in range( lastPrintedLevel, 1, -1 ):
         if lineNumber[level]:
            print '\n{: <{width}}'.format( '', width=pointerSize*2-1+(level-1)*3 ),
         print '}',
      CursorColumn = 0
      lastPrintedLevel = 0

   reentrancyLevel -= 1

class UdsDump( ):

   def __init__(self, debugger, address_str = None):
      global thread, pointerSize, target

      target = debugger.GetSelectedTarget( )
      # Set global thread for later use in command_function to execute memcmp
      thread = target.GetProcess().GetSelectedThread()
      # Set global integer size
      pointerSize = target.FindFirstType( 'void' ).GetPointerType( ).size

      frame = thread.GetFrameAtIndex( 0 )
      funcs = frame.GetFunctionName( )
      function = frame.GetFunction()
      #print "{func}".format( func='%s [inlined]' % funcs if frame.IsInlined() else funcs),

      whiteList = []
      for local_var in frame.get_arguments( ):
         if local_var.GetTypeName( ) == 'debug_dump_t':
            if local_var.value == 'DUMP_LIMITED_TO_EXPLICIT_LIST':
               some_string = target.FindFirstType( "char" ).GetPointerType( )
               DebugDumpWhiteListAddr = target.FindFirstGlobalVariable( "PcUtDebugDumpCurrent" ).GetValueAsUnsigned( )
               while DebugDumpWhiteListAddr != 0:
                  addr = lldb.SBAddress( DebugDumpWhiteListAddr, lldb.target )
                  DebugDumpWhiteListAddr += pointerSize
                  StringEntry = target.CreateValueFromAddress( "char", addr, some_string )
                  if StringEntry.GetValueAsUnsigned( ):
                     whiteList.append( StringEntry.GetSummary( ).translate( None, '"' ) )
                  else:
                     break

      if len( whiteList ):
         print '************************************************************************************************************************************'
         print '*                                                Limited APPLICATION DEBUG DUMP                                                    *'
         print '************************************************************************************************************************************'
      else:
         print '\n************************************************************************************************************************************'
         print '*                                         APPLICATION DEBUG DUMP starts with stack backtrace                                       *'
         print '************************************************************************************************************************************'
         lldbutils.print_stacktraces( target.GetProcess( ) )

      if target:
         # Keep track of which variables we have already looked up
         global_names = list()
         for xxx in range( 0, target.GetNumModules( ) ):
            printedHeader = False
            module_file_name = target.GetModuleAtIndex( xxx ).GetFileSpec( ).GetFilename( )
            if 'vdso' not in module_file_name and 'lldb' not in module_file_name and 'libc' not in module_file_name and 'linux' not in module_file_name:
               print
               # Get the executable module
               #module = target.module[target.executable.basename]
               module = target.module[module_file_name]
               if module:
                  # Iterate through all symbols in the symbol table and watch for any DATA symbols
                  for symbol in module.symbols:
                     if symbol.type == lldb.eSymbolTypeData:
                        # The symbol is a DATA symbol, lets try and find all global variables 
                        # that match this name and print them
                        global_name = symbol.name
                        # Make sure we don't lookup the same variable twice
                        if global_name not in global_names:
                           global_names.append(global_name)
                           # Find all global variables by name
                           global_variable_list = module.FindGlobalVariables(target, global_name, lldb.UINT32_MAX)
                           if global_variable_list:
                              # Print results for anything that matched
                              for global_variable in global_variable_list:
                                 if global_variable.name not in global_exclude_list:
                                    if len( whiteList ) and global_variable.name not in whiteList:
                                       continue
                                    if not printedHeader:
                                       print
                                       print '------------------------------------------------------------------------------------------------------------------------------------'
                                       print '                                          MODULE NAME: ', module_file_name
                                       print '------------------------------------------------------------------------------------------------------------------------------------'
                                       print '{'
                                       printedHeader = True
                                    # Check if this is an array
                                    extractNumber = re.search('\[(\d+)\]', global_variable.GetTypeName() )
                                    if extractNumber and int( extractNumber.group(1) ) == global_variable.GetNumChildren( ):
                                       genericVarPrint( global_variable, RecTypes.Array, 0, global_variable.GetNumChildren( ) )
                                    else:
                                       genericVarPrint( global_variable, RecTypes.Base, 0, 0 )
                                    #print 'name = %s' % global_variable.name    # returns the global variable name as a string
                                    #print 'value = %s' % global_variable.value  # Returns the variable value as a string
                                    #print 'type = %s' % global_variable.type    # Returns an lldb.SBType object
                                    #print 'addr = %s' % global_variable.addr    # Returns an lldb.SBAddress (section offset address) for this global
                                    #print 'file_addr = 0x%x' % global_variable.addr.file_addr    # Returns the file virtual address for this global
                                    #print 'location = %s' % global_variable.location    # returns the global variable value as a string
                                    #print 'size = %s' % global_variable.size    # Returns the size in bytes of this global variable
                                    #print
            if printedHeader:
               print '\n}'

      print '************************************************************************************************************************************'
      print '*                                             End of debug dump. Thanks for using LLDB.                                            *'
      print '************************************************************************************************************************************'



def udsdump( debugger, command, result, dict ):
   try:
       UdsDump( debugger, shlex.split( command ) )
   except:
       result.PutCString( "error: python exception %s" % sys.exc_info()[0] )


def zenBackTrace( debugger, command, result, dict ):
   global target, thread, pointerSize

   target = debugger.GetSelectedTarget( )
   thread = target.GetProcess().GetSelectedThread()
   # Set global integer size
   pointerSize = target.FindFirstType( 'void' ).GetPointerType( ).size

   lldbutils.print_stacktraces( target.GetProcess( ) )


def create_zenExpression_options():
   usage = "usage: %prog [options]"
   description = '''This command is meant to be an example of how to make an LLDB command that
does something useful, follows best practices, and exploits the SB API.
Specifically, this command computes the aggregate and average size of the variables in the current frame
and allows you to tweak exactly which variables are to be accounted in the computation.
'''
   parser = optparse.OptionParser(
      description=description,
      prog='zenExpression',
      usage=usage)
   parser.add_option(
      '-l',
      '--locals',
      action='store_true',
      dest='locals',
      help='locals = True',
      default=False)
   parser.add_option(
      '-s',
      '--statics',
      action='store_true',
      dest='statics',
      help='statics = True',
      default=False)
   return parser


def zenExpression( debugger, command, result, dict ):
   global thread, pointerSize, TopLevelArrayFoldingDisable, target

   # Use the Shell Lexer to properly parse up command options just like a
   # shell would
   command_args = shlex.split( command )
   parser = create_zenExpression_options( )
   try:
      ( options, args ) = parser.parse_args( command_args )
   except:
      # if you don't handle exceptions, passing an incorrect argument to the OptionParser will cause LLDB to exit
      # (courtesy of OptParse dealing with argument errors by throwing SystemExit)
      result.SetError("option parsing failed")
      return

   target = debugger.GetSelectedTarget( )
   thread = target.GetProcess().GetSelectedThread()
   if thread and thread.GetSelectedFrame():
      frame = thread.GetSelectedFrame()
   try:
      evaluated_name = frame.EvaluateExpression( command )
      #print 'type', evaluated_name.type
      #print 'GetTypeName', evaluated_name.GetTypeName( )
      #print 'addr', evaluated_name.addr
      #print 'addrOf', evaluated_name.AddressOf( ).GetValueAsUnsigned()
      #print 'GetLoadAddress', hex( evaluated_name.GetLoadAddress( ) )
      #print 'name', evaluated_name.name
      #print 'value', evaluated_name.value

      #genericVarPrint( evaluated_name, RecTypes.Base, 0, 0 )

      # temporarily disable folding of top level arrays
      TopLevelArrayFoldingDisable = 1

      extractNumber = re.search('\[(\d+)\]', evaluated_name.GetTypeName() )
      if extractNumber and int( extractNumber.group(1) ) == evaluated_name.GetNumChildren( ):
         genericVarPrint( evaluated_name, RecTypes.Array, 0, evaluated_name.GetNumChildren( ) )
      else:
         genericVarPrint( evaluated_name, RecTypes.Base, 0, 0 )
      print
      # Restore to default value for udsDump command.
      TopLevelArrayFoldingDisable = 0
   except:
       print 'Exception while evaluating', evaluated_name
       result.PutCString( "error: python exception %s" % sys.exc_info()[0] )


#def looper( frame, bp_loc, dict ):
# Use this prototype if making this function a callback on a breakpoint

def looper( debugger, command, exe_ctx, result, dict ):
   # This function is intended to be called on breakpoint in gdb_s_entry function
   # which is two levels down from code being debugged. It will expect
   # an array of strings to be passed to it as second parameter. Then it will
   # start executing each string as a debugger command.
   # dbg_s_entry can be called from qsmt_debugInfo or qsmt_assert functions which are 
   # one level down from the code being debugged. Code here only cares if a word "assert"
   # is present in the function name. It will affect wording in the header this code will produce.
   global thread, pointerSize, TopLevelArrayFoldingDisable, target

   try:
      target = exe_ctx.GetTarget()
      thread = exe_ctx.GetProcess().GetSelectedThread( )
      frame = thread.GetSelectedFrame()
      var = frame.get_arguments( )[1]
      if var.GetTypeName( ) == "char **":
         loop = 0
         # ci & ro from here: http://averagejake.com/post/xcoders-lldb-python-scripting/lldb-python-scripting.pdf and https://github.com/JakeCarter/lldb-scripts
         ci = debugger.GetCommandInterpreter( )
         ro = lldb.SBCommandReturnObject( )
         ci.HandleCommand( "up", ro )
         if "assert" in thread.GetSelectedFrame().GetFunction().name:
            string = "Assertion @ "
         else:
            string = "Debugger info @ "
         ci.HandleCommand( "up", ro )
         string += thread.GetSelectedFrame().GetLineEntry( ).GetFileSpec().GetFilename( )
         string += " : " + str( thread.GetSelectedFrame().GetLineEntry( ).GetLine( ) )
         if len( string ) > MAX_NUMBER_OF_CHARACTERS_IN_ONE_LINE:
            print string
         else:
            length = ( MAX_NUMBER_OF_CHARACTERS_IN_ONE_LINE - 12 - len( string ) ) / 2
            print "=" * length, string, "=" * length
         while True:
            cmd = var.name + "[" + str( loop ) + "]"
            cmd = frame.GetThread().GetProcess().ReadCStringFromMemory( frame.EvaluateExpression( cmd ).GetValueAsUnsigned( ), 0xffffff, lldb.SBError() )
            # cmd = cmd.strip()
            # className = ro.GetOutput().strip()
            if len( cmd ):
               print "cmd->\"" + cmd + "\"",
               ci.HandleCommand( cmd, ro )
               #print ro.GetOutput()
               loop += 1
            else:
               break
         print "=" * ( MAX_NUMBER_OF_CHARACTERS_IN_ONE_LINE - 10 )
   except:
       print 'Exception during looper command'
       result.PutCString( "error: python exception %s" % sys.exc_info()[0] )


def __lldb_init_module( debugger, dict ):
   # This initializer is being run from LLDB in the embedded command interpreter
   # Make the options so we can generate the help text for the new LLDB
   # command line command prior to registering it with LLDB below
   parser = create_zenExpression_options()
   #zenExpression.__doc__ = parser.format_help()
   # Add any commands contained in this module to LLDB
   debugger.HandleCommand( 'command script add -f ssd_udsDump.zenExpression p' )
   print 'The "zenExpression" command has been installed, type "help zenExpression" or "zenExpression --help" for detailed help.'

   debugger.HandleCommand( 'command script add -f ssd_udsDump.looper lp' )
   print 'The "lp" command has been installed, type "help lp" or "lp --help" for detailed help.'

   debugger.HandleCommand( 'command script add -f ssd_udsDump.zenBackTrace zbt' )
   print 'The "zenBackTrace" command has been installed, type "help zenBackTrace" or "zenBackTrace --help" for detailed help.'

   debugger.HandleCommand( 'command script add -f ssd_udsDump.udsdump udsdump' )
   print '"udsdump" command(s) are/is installed'

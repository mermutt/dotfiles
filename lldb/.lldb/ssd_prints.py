import optparse
import sys
import lldb
import shlex

class FmrPrint( ):
   def printNicely( self, FMR, called_from_counterpart ):
      ################################################################################
      #                        OUTPUT Link Next
      ################################################################################
      print FMR.GetName( ), '@0x%x' % FMR.AddressOf( ).GetValueAsUnsigned( )
      if FMR.AddressOf( ).GetValueAsUnsigned( ) == 0:
          return

      fmr_Link_Next = FMR.GetChildMemberWithName( "Link" ).GetChildMemberWithName( "Next" )

      if ( fmr_Link_Next.GetValueAsUnsigned( ) != 0 ):
          print ' Link { Next: %s }' % fmr_Link_Next.GetValue( ),

      print ' Flags={',
      # Flags Field
      fmr_Flags_Field = FMR.GetChildMemberWithName( "Flags" ).GetChildMemberWithName( "Field" )

      fmr_Flags_Field_MediaResponseData = fmr_Flags_Field.GetChildMemberWithName( "MediaResponseData" )
      if ( fmr_Flags_Field_MediaResponseData.GetValueAsUnsigned( ) != 0 ):
          print 'MediaResponseData:0x%x' % fmr_Flags_Field_MediaResponseData.GetValueAsUnsigned( ),
      fmr_Flags_Field_BusyWaitFMR = fmr_Flags_Field.GetChildMemberWithName( "BusyWaitFMR" )
      if ( fmr_Flags_Field_BusyWaitFMR.GetValueAsUnsigned( ) != 0 ):
          print ' BusyWaitFMR',
      fmr_Flags_Field_WantMcData = fmr_Flags_Field.GetChildMemberWithName( "WantMcData" )
      if ( fmr_Flags_Field_WantMcData.GetValueAsUnsigned( ) != 0 ):
          print ' WantMcData',
      fmr_Flags_Field_WantFMRData = fmr_Flags_Field.GetChildMemberWithName( "WantFMRData" )
      if ( fmr_Flags_Field_WantFMRData.GetValueAsUnsigned( ) != 0 ):
          print ' WantFMRData',
      fmr_Flags_Field_QueuedForComplete = fmr_Flags_Field.GetChildMemberWithName( "QueuedForComplete" )
      if ( fmr_Flags_Field_QueuedForComplete.GetValueAsUnsigned( ) != 0 ):
          print ' QueuedForComplete',
      fmr_Flags_Field_WriteXfrComplete = fmr_Flags_Field.GetChildMemberWithName( "WriteXfrComplete" )
      if ( fmr_Flags_Field_WriteXfrComplete.GetValueAsUnsigned( ) != 0 ):
          print ' WriteXfrComplete',
      fmr_Flags_Field_RequestComplete = fmr_Flags_Field.GetChildMemberWithName( "RequestComplete" )
      if ( fmr_Flags_Field_RequestComplete.GetValueAsUnsigned( ) != 0 ):
          print ' RequestComplete',
      fmr_Flags_Field_RequestAbort = fmr_Flags_Field.GetChildMemberWithName( "RequestAbort" )
      if ( fmr_Flags_Field_RequestAbort.GetValueAsUnsigned( ) != 0 ):
          print ' RequestAbort',
      fmr_Flags_Field_SmallReadIndex = fmr_Flags_Field.GetChildMemberWithName( "SmallReadIndex")
      if ( fmr_Flags_Field_SmallReadIndex.GetValueAsUnsigned( ) != 0 ):
          print ' SmallReadIndex:%d' % fmr_Flags_Field_SmallReadIndex.GetValueAsUnsigned( ),
      print '}'

      print '   PsmReq {',
      # PsmReq
      fmr_PsmReq = FMR.GetChildMemberWithName( "PsmReq" )
      # PsmReq CmdCode Field
      fmr_PsmReq_CmdCode_Field = fmr_PsmReq.GetChildMemberWithName( "CmdCode" ).GetChildMemberWithName( "Field" )

      fmr_PsmReq_CmdCode_Field_CmdCode       = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "CmdCode" )
      print 'CmdCode:%s' % fmr_PsmReq_CmdCode_Field_CmdCode.GetValue( ),

      fmr_PsmReq_CmdCode_Field_IoedcEnabled  = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "IoedcEnabled" )
      if ( fmr_PsmReq_CmdCode_Field_IoedcEnabled.GetValueAsUnsigned( ) ):
          print '| IoedcEnabled',

      fmr_PsmReq_CmdCode_Field_MSBCommand    = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "MSBCommand" )
      if ( fmr_PsmReq_CmdCode_Field_MSBCommand.GetValueAsUnsigned( ) ):
          print '| MSBCommand',

      fmr_PsmReq_CmdCode_Field_ResetRunt     = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "ResetRunt" )
      if ( fmr_PsmReq_CmdCode_Field_ResetRunt.GetValueAsUnsigned( ) ):
          print '| ResetRunt',
      fmr_PsmReq_CmdCode_Field_PmuHeaders    = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "PmuHeaders" )
      if ( fmr_PsmReq_CmdCode_Field_PmuHeaders.GetValueAsUnsigned( ) ):
          print '| PmuHeaders',

      fmr_PsmReq_CmdCode_Field_SystemSector  = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "SystemSector" )
      if ( fmr_PsmReq_CmdCode_Field_SystemSector.GetValueAsUnsigned( ) ):
          print '| SystemSector',

      fmr_PsmReq_CmdCode_Field_EndOfStripe   = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "EndOfStripe" )
      if ( fmr_PsmReq_CmdCode_Field_EndOfStripe.GetValueAsUnsigned( ) ):
          print '| EndOfStripe',
      fmr_PsmReq_CmdCode_Field_FormatTable   = fmr_PsmReq_CmdCode_Field.GetChildMemberWithName( "FormatTable" )
      print '| FormatTable:%s' % fmr_PsmReq_CmdCode_Field_FormatTable.GetValueAsUnsigned( ),

      # PsmReq FlashAddress Field
      fmr_PsmReq_FlashAddress_Field = fmr_PsmReq.GetChildMemberWithName( "FlashAddress" ).GetChildMemberWithName( "Field" )
      fmr_PsmReq_FlashAddress_Field_Page  = fmr_PsmReq_FlashAddress_Field.GetChildMemberWithName( "Page" )
      fmr_PsmReq_FlashAddress_Field_Block = fmr_PsmReq_FlashAddress_Field.GetChildMemberWithName( "Block" )
      fmr_PsmReq_FlashAddress_Field_Die   = fmr_PsmReq_FlashAddress_Field.GetChildMemberWithName( "Die" )
      fmr_PsmReq_Block = fmr_PsmReq.GetChildMemberWithName( "Block" ).GetChildAtIndex( 0 )
      print '| Die:%d Block:0x%x/0x%x Page:0x%x' % (
              fmr_PsmReq_FlashAddress_Field_Die.GetValueAsUnsigned( ),
              fmr_PsmReq_FlashAddress_Field_Block.GetValueAsUnsigned( ),
              fmr_PsmReq_Block.GetValueAsUnsigned( ),
              fmr_PsmReq_FlashAddress_Field_Page.GetValueAsUnsigned( ) ),

      fmr_PsmReq_FlashAddress_Field_RuntBuffer = fmr_PsmReq_FlashAddress_Field.GetChildMemberWithName( "RuntBuffer" )
      print '| %s }' % fmr_PsmReq_FlashAddress_Field_RuntBuffer.GetValue( ),

      fmr_ReqHandlePtr = FMR.GetChildMemberWithName( "ReqHandlePtr" )
      print ' ReqHandlePtr:', fmr_ReqHandlePtr.GetValue()
      if ( ( called_from_counterpart != True ) and fmr_ReqHandlePtr.GetValueAsUnsigned( ) ):
          ReqHandlePrint( fmr_ReqHandlePtr.GetValue( ), True )

   def __init__(self, fmr_address, called_from_counterpart = None ):
      target = lldb.debugger.GetSelectedTarget( )

      flash_media_req = target.FindFirstType( 'flash_media_req' )
      fmr_addr = lldb.SBAddress( int( fmr_address, 0 ), lldb.target )
      FMR = target.CreateValueFromAddress( "flash_media_req *", fmr_addr, flash_media_req )

      self.printNicely( FMR, called_from_counterpart )

class ReqHandlePrint( ):

   def printNicely( self, ReqHandle, called_from_counterpart ):
      ################################################################################
      #                        OUTPUT Link Next
      ################################################################################
      print ReqHandle.GetName( ), '@0x%x' % ReqHandle.AddressOf( ).GetValueAsUnsigned( )
      if ReqHandle.AddressOf( ).GetValueAsUnsigned( ) == 0:
          return

      rh_Link_Next = ReqHandle.GetChildMemberWithName( "Link" ).GetChildMemberWithName( "Next" )
      if ( rh_Link_Next.GetValueAsUnsigned( ) ):
          print ' Next: %s' % rh_Link_Next.GetValue( ),

      # CommonData
      rh_CommonData = ReqHandle.GetChildMemberWithName( "CommonData" )
      # CommonData.Flags
      rh_CommonData_Flags_Field = rh_CommonData.GetChildMemberWithName( "Flags" ).GetChildMemberWithName( "Field" )
      print '  Flags={ Bus:%d' % rh_CommonData_Flags_Field.GetChildMemberWithName( "Bus" ).GetValueAsUnsigned( ),
      print '| %s' % ( rh_CommonData_Flags_Field.GetChildMemberWithName( "Type" ).GetValue( ) ),
      print '| GCU:0x%04x' % ( rh_CommonData.GetChildMemberWithName( "GcuIndex" ).GetValueAsUnsigned( ) ),
      print '| %s' % ( rh_CommonData_Flags_Field.GetChildMemberWithName( "FtlDataType" ).GetValue( ) ),
      print '| %s' % ( rh_CommonData_Flags_Field.GetChildMemberWithName( "State" ).GetValue( ) ),

      SpanIn = rh_CommonData_Flags_Field.GetChildMemberWithName( "SpanIn" ).GetValueAsUnsigned( )
      SpanOut = rh_CommonData_Flags_Field.GetChildMemberWithName( "SpanOut" ).GetValueAsUnsigned( )
      if ( SpanIn != 0 ) or ( SpanOut != 0 ):
          print '| Span(%d/%d)' % ( SpanIn, SpanOut ),
      print ' }'

      # CommonData.Response.Sense
      rh_CommonData_Response_Sense = rh_CommonData.GetChildMemberWithName( "Response" ).GetChildMemberWithName( "Sense" )
      print '   %s' % ( rh_CommonData_Response_Sense.GetChildMemberWithName( "Status" ).GetValue( ) ),
      if ( rh_CommonData_Response_Sense.GetChildMemberWithName( "Status" ).GetValue( ) != "RW_REQUEST_SUCCESSFUL" ):
          print '0x%x' % rh_CommonData_Response_Sense.GetChildMemberWithName( "ErrorCode" ).GetValueAsUnsigned( ),

      print ' Flags2={',
      # CommonData.Flags2
      rh_CommonData_Flags2_Field = rh_CommonData.GetChildMemberWithName( "Flags2" ).GetChildMemberWithName( "Field" )
      XfrLenInPhyMapUnits = rh_CommonData_Flags2_Field.GetChildMemberWithName( "XfrLenInPhyMapUnits" ).GetValueAsUnsigned( )
      #print '| XfrLenInPhyMapUnits:%d' % XfrLenInPhyMapUnits,
      if ( rh_CommonData_Flags2_Field.GetChildMemberWithName( "KeepBuffer" ).GetValueAsUnsigned( ) ):
          print '| KeepBuffer',
      if ( rh_CommonData_Flags2_Field.GetChildMemberWithName( "SpanFMRComplete" ).GetValueAsUnsigned( ) ):
          print '| SpanFMRComplete',
      if ( rh_CommonData_Flags2_Field.GetChildMemberWithName( "RecoveryAttempted" ).GetValueAsUnsigned( ) ):
          print '| RecoveryAttempted:%d' % rh_CommonData_Flags2_Field.GetChildMemberWithName( "RecoveryAttempted" ).GetValueAsUnsigned( ),
      if ( rh_CommonData_Flags2_Field.GetChildMemberWithName( "FormatTable" ).GetValueAsUnsigned( ) ):
          print '| FormatTable:%d' % rh_CommonData_Flags2_Field.GetChildMemberWithName( "FormatTable" ).GetValueAsUnsigned( ),
      print '| XfrLenInPages:%x }' % rh_CommonData_Flags2_Field.GetChildMemberWithName( "XfrLenInPages" ).GetValueAsUnsigned( ),

      # CommonData.PmuFlags
      rh_CommonData_PmuFlags = rh_CommonData.GetChildMemberWithName( "PmuFlags" )
      if ( rh_CommonData_PmuFlags.GetChildMemberWithName( "Mode" ).GetChildMemberWithName( "Mode" ).GetValueAsUnsigned( ) == 0 ):
          rh_CommonData_PmuFlags_SectorMaskMode = rh_CommonData_PmuFlags.GetChildMemberWithName( "SectorMaskMode" )
          print ' Sector Mask:0x%x' % rh_CommonData_PmuFlags_SectorMaskMode.GetChildMemberWithName( "SectorMask" ).GetValueAsUnsigned( ),
          print '| StartMuOffset:0x%x' % rh_CommonData_PmuFlags_SectorMaskMode.GetChildMemberWithName( "StartMuOffset" ).GetValueAsUnsigned( ),
          BlkIdCount = 8
      else:
          rh_CommonData_PmuFlags_MuMaskMode = rh_CommonData_PmuFlags.GetChildMemberWithName( "MUMaskMode" ).GetChildMemberWithName( "MuMask" )
          print ' MuMask:0x%x' % ( rh_CommonData_PmuFlags_MuMaskMode.GetValueAsUnsigned( ) ),
          BlkIdCount = XfrLenInPhyMapUnits

      if BlkIdCount:
          # CommonData.PmuInfo
          rh_CommonData_PmuInfo = rh_CommonData.GetChildMemberWithName( "PmuInfo" )
          print '\n   PMU/BlkId[%d]' % BlkIdCount,
          for num in range( 0, BlkIdCount ):
              print ' [%d]:0x%x/0x%x' % ( num, rh_CommonData_PmuInfo.GetChildAtIndex( num ).GetChildMemberWithName( "PMU" ).GetChildMemberWithName( "lwrd" ).GetValueAsUnsigned( ), rh_CommonData_PmuInfo.GetChildAtIndex( num ).GetChildMemberWithName( "BlkID" ).GetChildMemberWithName( "lwrd" ).GetValueAsUnsigned( ) ),

      if BlkIdCount > 3:
          # Add new line if more than 3 vbm/pmu pairs printed
          print

      if SpanIn != 0 or SpanOut != 0 :
          # CommonData.SpanningInfo
          rh_CommonData_SpanningInfo = ReqHandle.GetChildMemberWithName( "SpanningInfo" )
          print '   SpanningInfo{ PMU/VbmIndex:0x%x/0x%x' % ( rh_CommonData_SpanningInfo.GetChildMemberWithName( "PMU" ).GetValueAsUnsigned( ), rh_CommonData_SpanningInfo.GetChildMemberWithName( "VbmIndex" ).GetValueAsUnsigned( ) ),
          print '| FirstRH:0x%x' % rh_CommonData_SpanningInfo.GetChildMemberWithName( "FirstRH" ).GetValueAsUnsigned( ),
          SpanningInfo_CorruptedMask = rh_CommonData_SpanningInfo.GetChildMemberWithName( "CorruptedMask" ).GetValueAsUnsigned( ),
          if ( SpanningInfo_CorruptedMask != 0 ):
              print '| CorruptedMask:0x%x' % SpanningInfo_CorruptedMask,
          print '}',
      
      # Getting FLRs from ParentReqPtr
      flash_logical_req = lldb.debugger.GetSelectedTarget( ).FindFirstType( 'flash_logical_req' )
      addr = lldb.SBAddress( ReqHandle.GetChildMemberWithName( "ParentReqPtr" ).GetChildAtIndex( 0 ).GetValueAsUnsigned( ), lldb.target )
      FLR = lldb.debugger.GetSelectedTarget( ).CreateValueFromAddress( "flash_logical_req *", addr, flash_logical_req )
      if FLR:
          print 'ParentReqPtr[0]:0x%x XfrOpts:0x%x' % ( FLR.AddressOf( ).GetValueAsUnsigned( ), FLR.GetChildMemberWithName( "MediaXfrReq" ).GetChildMemberWithName( "XfrAndBufOptions" ).GetValueAsUnsigned( ) ),

      print
      # CommonData.FlashMediaReqCallbackPtr
      rh_CommonData_FlashMediaReqCallbackPtr = ReqHandle.GetChildMemberWithName( "FlashMediaReqCallbackPtr" )
      # Symbolicating callback pointer
      so_addr = lldb.target.ResolveLoadAddress( rh_CommonData_FlashMediaReqCallbackPtr.GetValueAsUnsigned( ) )
      symbol = lldb.target.ResolveSymbolContextForAddress( so_addr, lldb.eSymbolContextEverything ).GetSymbol()
      print '  ', symbol.GetName(),

      # CommonData.ParentFMR
      rh_CommonData_ParentFMR = ReqHandle.GetChildMemberWithName( "ParentFMR" )
      print '| ParentFMR 0x%x' % rh_CommonData_ParentFMR.GetValueAsUnsigned( ),

      # CommonData.PendingOperations
      rh_CommonData_PendingOperations = ReqHandle.GetChildMemberWithName( "PendingOperations" )
      if rh_CommonData_PendingOperations.GetValueAsUnsigned( ):
          print '| PendingOperations:%d' % rh_CommonData_PendingOperations.GetValueAsUnsigned( ),

      # CommonData.StartingGcuPmuOffset
      rh_CommonData_StartingGcuPmuOffset = ReqHandle.GetChildMemberWithName( "StartingGcuPmuOffset" )
      print '| StartingGcuPmuOffset:0x%x' % rh_CommonData_StartingGcuPmuOffset.GetValueAsUnsigned( )

      if called_from_counterpart != True and rh_CommonData_ParentFMR.GetValueAsUnsigned( ):
          FmrPrint( rh_CommonData_ParentFMR.GetValue( ), True )

   def __init__(self, rh_address, called_from_counterpart = None ):
      target = lldb.debugger.GetSelectedTarget( )

      flash_media_req_handle = target.FindFirstType( 'flash_media_req_handle' )

      addr = lldb.SBAddress( int( rh_address, 0 ), lldb.target )
      TestRH = target.CreateValueFromAddress( "flash_media_req_handle *", addr, flash_media_req_handle )

      self.printNicely( TestRH, called_from_counterpart )

class BxorReqPrint( ):

   def printNicely( self, BxorReq ):
      ################################################################################
      #                        OUTPUT Link Next
      ################################################################################
      print BxorReq.GetName( ), '@0x%x' % BxorReq.AddressOf( ).GetValueAsUnsigned( ),
      if BxorReq.AddressOf( ).GetValueAsUnsigned( ) == 0:
          return

      BxorReq_Link_Next = BxorReq.GetChildMemberWithName( "Link" ).GetChildMemberWithName( "Next" )
      if ( BxorReq_Link_Next.GetValueAsUnsigned( ) ):
          print ' Next: %s' % BxorReq_Link_Next.GetValue( ),

      print ' BxorFlags={',
      # BxorFlags.Field
      BxorReq_BxorFlags_Field = BxorReq.GetChildMemberWithName( "BxorFlags" ).GetChildMemberWithName( "Field" )

      BxorReq_BxorFlags_Field_UseMask = BxorReq_BxorFlags_Field.GetChildMemberWithName( "UseMask" )
      if BxorReq_BxorFlags_Field_UseMask.GetValueAsUnsigned( ):
          print ' UseMask:0x%x' % BxorReq_BxorFlags_Field_UseMask.GetValueAsUnsigned( ),

      BxorReq_BxorFlags_Field_PackDestData = BxorReq_BxorFlags_Field.GetChildMemberWithName( "PackDestData" )
      if BxorReq_BxorFlags_Field_PackDestData.GetValueAsUnsigned( ):
          print '| PackDestData' % BxorReq_BxorFlags_Field_PackDestData.GetValueAsUnsigned( ),

      BxorReq_BxorFlags_Field_State = BxorReq_BxorFlags_Field.GetChildMemberWithName( "State" )
      print '|', BxorReq_BxorFlags_Field_State.GetValue( ),

      BxorReq_BxorFlags_Field_Type = BxorReq_BxorFlags_Field.GetChildMemberWithName( "Type" )
      print '|', BxorReq_BxorFlags_Field_Type.GetValue( ),

      BxorReq_BxorFlags_Field_XorCompletionStatus = BxorReq_BxorFlags_Field.GetChildMemberWithName( "XorCompletionStatus" )
      print '|', BxorReq_BxorFlags_Field_XorCompletionStatus.GetValue( ),

      BxorReq_BxorFlags_Field_JournalOutercodeBufIndex = BxorReq_BxorFlags_Field.GetChildMemberWithName( "JournalOutercodeBufIndex" )
      if BxorReq_BxorFlags_Field_JournalOutercodeBufIndex.GetValueAsUnsigned( ):
          print '| JournalOutercodeBufIndex:0x%x' % BxorReq_BxorFlags_Field_JournalOutercodeBufIndex.GetValueAsUnsigned( ),

      BxorReq_BxorFlags_Field_DropRequestDuringPFail = BxorReq_BxorFlags_Field.GetChildMemberWithName( "DropRequestDuringPFail" )
      if BxorReq_BxorFlags_Field_DropRequestDuringPFail.GetValueAsUnsigned( ):
          print '| DropRequestDuringPFail',

      BxorReq_BxorFlags_Field_PackSourceData = BxorReq_BxorFlags_Field.GetChildMemberWithName( "PackSourceData" )
      if BxorReq_BxorFlags_Field_PackSourceData.GetValueAsUnsigned( ):
          print '| PackSourceData',

      print '}'

      print ' Request={',
      if ( BxorReq_BxorFlags_Field_Type.GetValue( ) == 'COPY_DATA' ):
          # BxorReq.XOR.XxxRequest
          BxorReq_Request = BxorReq.GetChildMemberWithName( "XOR" ).GetChildMemberWithName( "CopyRequest" )
          # BxorReq.XOR.XxxRequest.SourceAddress
          BxorReq_Request_SourceAddress = BxorReq_Request.GetChildMemberWithName( "SourceAddress" )
          # BxorReq.XOR.XxxRequest.DestinationAddress
          BxorReq_Request_DestinationAddress = BxorReq_Request.GetChildMemberWithName( "DestinationAddress" )

          # BxorReq.XOR.XxxRequest.BufferMode
          BxorReq_Request_BufferMode_int = BxorReq_Request.GetChildMemberWithName( "BufferMode" ).GetValueAsUnsigned( )
          if BxorReq_Request_BufferMode_int > 1:
              BxorReq_Request_SourceAddress_int = BxorReq_Request_SourceAddress.GetChildMemberWithName( "VBMBufferIndex" ).GetValueAsUnsigned( )
              BxorReq_Request_DestinationAddress_int = BxorReq_Request_DestinationAddress.GetChildMemberWithName( "VBMBufferIndex" ).GetValueAsUnsigned( )
              print 'VBM 0x%x < 0x%x' % ( BxorReq_Request_DestinationAddress_int, BxorReq_Request_SourceAddress_int ),
          else:
              BxorReq_Request_SourceAddress_int = BxorReq_Request_SourceAddress.GetChildMemberWithName( "PhysicalBufferAddress" ).GetValueAsUnsigned( )
              BxorReq_Request_DestinationAddress_int = BxorReq_Request_DestinationAddress.GetChildMemberWithName( "PhysicalBufferAddress" ).GetValueAsUnsigned( )
              print 'Legacy 0x%x < 0x%x' % ( BxorReq_Request_DestinationAddress_int, BxorReq_Request_SourceAddress_int ),

          # BxorReq.XOR.XxxRequest.StartLBA
          BxorReq_Request_StartLBA_int = BxorReq_Request.GetChildMemberWithName( "StartLBA" ).GetValueAsUnsigned( )
          print '| StartLBA 0x%x' % BxorReq_Request_StartLBA_int,

          # BxorReq.XOR.XxxRequest.TransferLengthInSectors
          BxorReq_Request_TransferLengthInSectors_int = BxorReq_Request.GetChildMemberWithName( "TransferLengthInSectors" ).GetValueAsUnsigned( )
          print '| TransferLengthInSectors %d' % BxorReq_Request_TransferLengthInSectors_int,

          # BxorReq.XOR.XxxRequest.MemoryProtectionOptions
          BxorReq_Request_MemoryProtectionOptions = BxorReq_Request.GetChildMemberWithName( "MemoryProtectionOptions" )
          print '|%s' % BxorReq_Request_MemoryProtectionOptions.GetValue( ),

      elif ( BxorReq_BxorFlags_Field_Type.GetValue( ) == 'XOR_DATA' ):
          # BxorReq.XOR.XxxRequest
          BxorReq_Request = BxorReq.GetChildMemberWithName( "XOR" ).GetChildMemberWithName( "XfrRequest" )
          print 'XOR_DATA'

      print '}'

      # BxorReq.FlashMediaReq
      BxorReq_FlashMediaReq = BxorReq.GetChildMemberWithName( "FlashMediaReq" )
      print ' FlashMediaReq:0x%x' % BxorReq_FlashMediaReq.GetValueAsUnsigned( ),
      # BxorReq.BxorRequestCallbackPtr
      BxorReq_BxorRequestCallbackPtr = BxorReq.GetChildMemberWithName( "BxorRequestCallbackPtr" )
      so_addr = lldb.target.ResolveLoadAddress( BxorReq_BxorRequestCallbackPtr.GetValueAsUnsigned( ) )
      symbol = lldb.target.ResolveSymbolContextForAddress( so_addr, lldb.eSymbolContextEverything ).GetSymbol()
      print '|', symbol.GetName(),
      # BxorReq.SectorMask
      BxorReq_SectorMask = BxorReq.GetChildMemberWithName( "SectorMask" )
      print '| SectorMask:0x%x' % BxorReq_SectorMask.GetValueAsUnsigned( ),
      # BxorReq.StartBit
      BxorReq_StartBit = BxorReq.GetChildMemberWithName( "StartBit" )
      print '| StartBit:0x%x' % BxorReq_StartBit.GetValueAsUnsigned( )

      #lldb.debugger.HandleCommand( "script target = lldb.debugger.GetSelectedTarget( ); BxorReq = target.FindFirstGlobalVariable( 'BxorMgr' ).GetChildMemberWithName( 'ActiveRequest' ); BxorReq_StartBit = BxorReq.GetChildMemberWithName( 'StartBit' ); help BxorReq_StartBit" )

   def __init__(self, BxorReq_addr ):
      target = lldb.debugger.GetSelectedTarget( )

      bxor_req = target.FindFirstType( "bxor_req" )
      addr = lldb.SBAddress( int( BxorReq_addr, 0 ), lldb.target )
      BxorReq = target.CreateValueFromAddress( "bxor_req *", addr, bxor_req )

      self.printNicely( BxorReq )

class ErrRecMgrPrint( ):

   def printNicely( self, ErrRecMgr ):
      ################################################################################
      #                        OUTPUT
      ################################################################################
      print ErrRecMgr.GetType( )

      ErrRecMgr_RecoveryMediaReq = ErrRecMgr.GetChildMemberWithName( 'RecoveryMediaReq' )
      print '  RecoveryMediaReq: 0x%x' % ErrRecMgr_RecoveryMediaReq.GetValueAsUnsigned( )

      ErrRecMgr_ErrorRecoverySentinel_Next = ErrRecMgr.GetChildMemberWithName( "ErrorRecoverySentinel" ).GetChildMemberWithName( "Next" )
      print '  ErrorRecoverySentinel: 0x%x -> num elements' % ErrRecMgr_ErrorRecoverySentinel_Next.GetValueAsUnsigned( ),
      print WalkLinksAtSentinel( ErrRecMgr_ErrorRecoverySentinel_Next.AddressOf( ).GetValue(), 'stx_single_link_sentinel' )

      ErrRecMgr_IncomingFailedRequestSentinel_Next = ErrRecMgr.GetChildMemberWithName( "IncomingFailedRequestSentinel" ).GetChildMemberWithName( "Next" )
      print '  IncomingFailedRequestSentinel: 0x%x -> num elements' % ErrRecMgr_IncomingFailedRequestSentinel_Next.GetValueAsUnsigned( ),
      print WalkLinksAtSentinel( ErrRecMgr_IncomingFailedRequestSentinel_Next.AddressOf( ).GetValue(), 'stx_single_link_sentinel' )

      ErrRecMgr_LocalFailedRequestSentinel_Next = ErrRecMgr.GetChildMemberWithName( "LocalFailedRequestSentinel" ).GetChildMemberWithName( "Next" )
      print '  LocalFailedRequestSentinel: 0x%x -> num elements' % ErrRecMgr_LocalFailedRequestSentinel_Next.GetValueAsUnsigned( ),
      print WalkLinksAtSentinel( ErrRecMgr_LocalFailedRequestSentinel_Next.AddressOf( ).GetValue(), 'stx_single_link_sentinel' )

      if ErrRecMgr.GetChildMemberWithName( 'KeepMediaRequest' ).GetValueAsUnsigned( ):
          print '  KeepMediaRequest'

      ErrRecMgr_OutercodeData = ErrRecMgr.GetChildMemberWithName( "OutercodeData" )
      print '  OutercodeData:'
      ErrRecMgr_OutercodeData_CurrentOffset = ErrRecMgr_OutercodeData.GetChildMemberWithName( "CurrentOffset" )
      print '   ', ErrRecMgr_OutercodeData_CurrentOffset.GetName( ), '=', ErrRecMgr_OutercodeData_CurrentOffset.GetValue( )

      ErrRecMgr_OutercodeData_ProcessedSegments = ErrRecMgr_OutercodeData.GetChildMemberWithName( "ProcessedSegments" )
      print '   ', ErrRecMgr_OutercodeData_ProcessedSegments.GetName( ), '=', ErrRecMgr_OutercodeData_ProcessedSegments.GetValue( )
      ErrRecMgr_OutercodeData_NumOutstandingXor = ErrRecMgr_OutercodeData.GetChildMemberWithName( "NumOutstandingXor" )
      print '   ', ErrRecMgr_OutercodeData_NumOutstandingXor.GetName( ), '=', ErrRecMgr_OutercodeData_NumOutstandingXor.GetValue( )
      ErrRecMgr_OutercodeData_PmuIndex = ErrRecMgr_OutercodeData.GetChildMemberWithName( "PmuIndex" )
      print '   ', ErrRecMgr_OutercodeData_PmuIndex.GetName( ), '=', ErrRecMgr_OutercodeData_PmuIndex.GetValue( )
      ErrRecMgr_OutercodeData_PageToRebuild = ErrRecMgr_OutercodeData.GetChildMemberWithName( "PageToRebuild" )
      print '   ', ErrRecMgr_OutercodeData_PageToRebuild.GetName( ), '=', ErrRecMgr_OutercodeData_PageToRebuild.GetValue( )
      ErrRecMgr_OutercodeData_OutstandingRead = ErrRecMgr_OutercodeData.GetChildMemberWithName( "OutstandingRead" )
      print '   ', ErrRecMgr_OutercodeData_OutstandingRead.GetName( ), '=', ErrRecMgr_OutercodeData_OutstandingRead.GetValue( )
      ErrRecMgr_OutercodeData_RebuildFailure = ErrRecMgr_OutercodeData.GetChildMemberWithName( "RebuildFailure" )
      print '   ', ErrRecMgr_OutercodeData_RebuildFailure.GetName( ), '=', ErrRecMgr_OutercodeData_RebuildFailure.GetValue( )
      ErrRecMgr_OutercodeData_BxorOffset = ErrRecMgr_OutercodeData.GetChildMemberWithName( "BxorOffset" )
      print '   ', ErrRecMgr_OutercodeData_BxorOffset.GetName( ), '=', ErrRecMgr_OutercodeData_BxorOffset.GetValue( )

      ErrRecMgr_OutercodeData_BlockIDForPage = ErrRecMgr_OutercodeData.GetChildMemberWithName( "BlockIDForPage" )
      ErrRecMgr_OutercodeData_NumPmuVbmPairsForCheckIOEDC = ErrRecMgr_OutercodeData.GetChildMemberWithName( "NumPmuVbmPairsForCheckIOEDC" )

      print '    Vbm/Lba pairs',
      for indx in range( 0, ErrRecMgr_OutercodeData_NumPmuVbmPairsForCheckIOEDC.GetValueAsUnsigned( ) + 1 ):
          print '[%d]0x%x/0x%x' % ( indx,
                  ErrRecMgr_OutercodeData_BlockIDForPage.GetChildAtIndex( indx ).GetChildMemberWithName( "BlockID" ).GetValueAsUnsigned( ),
                  ErrRecMgr_OutercodeData_BlockIDForPage.GetChildAtIndex( indx ).GetChildMemberWithName( "Lba" ).GetValueAsUnsigned( )
                  ),
      print

      ErrRecMgr_OutercodeData_PmuVbmPairIndexInReq = ErrRecMgr_OutercodeData.GetChildMemberWithName( "PmuVbmPairIndexInReq" )
      print '   ', ErrRecMgr_OutercodeData_PmuVbmPairIndexInReq.GetName( ), '=', ErrRecMgr_OutercodeData_PmuVbmPairIndexInReq.GetValue( )
      ErrRecMgr_OutercodeData_PmuVbmPairIndexInList = ErrRecMgr_OutercodeData.GetChildMemberWithName( "PmuVbmPairIndexInList" )
      print '   ', ErrRecMgr_OutercodeData_PmuVbmPairIndexInList.GetName( ), '=', ErrRecMgr_OutercodeData_PmuVbmPairIndexInList.GetValue( )

      print '   ', ErrRecMgr_OutercodeData_NumPmuVbmPairsForCheckIOEDC.GetName( ), '=', ErrRecMgr_OutercodeData_NumPmuVbmPairsForCheckIOEDC.GetValue( )

      ErrRecMgr_OutercodeData_Flags_Filed = ErrRecMgr_OutercodeData.GetChildMemberWithName( "Flags" ).GetChildMemberWithName( "Field" )
      print '   ', ErrRecMgr_OutercodeData_Flags_Filed
      ErrRecMgr_OutercodeData_Plane = ErrRecMgr_OutercodeData.GetChildMemberWithName( "Plane" )
      print '   ', ErrRecMgr_OutercodeData_Plane.GetName( ), '=', ErrRecMgr_OutercodeData_Plane.GetValue( )
      ErrRecMgr_OutercodeData_TotalPages = ErrRecMgr_OutercodeData.GetChildMemberWithName( "TotalPages" )
      print '   ', ErrRecMgr_OutercodeData_TotalPages.GetName( ), '=', ErrRecMgr_OutercodeData_TotalPages.GetValue( )
      ErrRecMgr_OutercodeData_ErasedPagesInStripe = ErrRecMgr_OutercodeData.GetChildMemberWithName( "ErasedPagesInStripe" )
      print '   ', ErrRecMgr_OutercodeData_ErasedPagesInStripe.GetName( ), '=', ErrRecMgr_OutercodeData_ErasedPagesInStripe.GetValue( )
      ErrRecMgr_OutercodeData_BadPlaneBitMap = ErrRecMgr_OutercodeData.GetChildMemberWithName( "BadPlaneBitMap" )
      print '   ', ErrRecMgr_OutercodeData_BadPlaneBitMap.GetName( ), '=', ErrRecMgr_OutercodeData_BadPlaneBitMap.GetValue( )
      ErrRecMgr_OutercodeData_AnotherPageErrorCode = ErrRecMgr_OutercodeData.GetChildMemberWithName( "AnotherPageErrorCode" )
      print '   ', ErrRecMgr_OutercodeData_AnotherPageErrorCode.GetName( ), '=', ErrRecMgr_OutercodeData_AnotherPageErrorCode.GetValue( )
      ErrRecMgr_OutercodeData_SpanningInPageRead = ErrRecMgr_OutercodeData.GetChildMemberWithName( "SpanningInPageRead" )
      print '   ', ErrRecMgr_OutercodeData_SpanningInPageRead.GetName( ), '=', ErrRecMgr_OutercodeData_SpanningInPageRead.GetValue( )
      ErrRecMgr_OutercodeData_ActiveWrtCntr = ErrRecMgr_OutercodeData.GetChildMemberWithName( "ActiveWrtCntr" )
      print '   ', ErrRecMgr_OutercodeData_ActiveWrtCntr.GetName( ), '=', ErrRecMgr_OutercodeData_ActiveWrtCntr.GetValue( )
      ErrRecMgr_OutercodeData_XorPageStride = ErrRecMgr_OutercodeData.GetChildMemberWithName( "XorPageStride" )
      print '   ', ErrRecMgr_OutercodeData_XorPageStride.GetName( ), '=', ErrRecMgr_OutercodeData_XorPageStride.GetValue( )
      ErrRecMgr_OutercodeData_BusToDoMask = ErrRecMgr_OutercodeData.GetChildMemberWithName( "BusToDoMask" )
      print '   ', ErrRecMgr_OutercodeData_BusToDoMask.GetName( ), '=', ErrRecMgr_OutercodeData_BusToDoMask.GetValue( )
      ErrRecMgr_OutercodeData_BusDoneMask = ErrRecMgr_OutercodeData.GetChildMemberWithName( "BusDoneMask" )
      print '   ', ErrRecMgr_OutercodeData_BusDoneMask.GetName( ), '=', ErrRecMgr_OutercodeData_BusDoneMask.GetValue( )
      ErrRecMgr_OutercodeData_CurrentBus = ErrRecMgr_OutercodeData.GetChildMemberWithName( "CurrentBus" )
      print '   ', ErrRecMgr_OutercodeData_CurrentBus.GetName( ), '=', ErrRecMgr_OutercodeData_CurrentBus.GetValue( )
      ErrRecMgr_OutercodeData_ErasedPageOffset = ErrRecMgr_OutercodeData.GetChildMemberWithName( "ErasedPageOffset" )
      print '   ', ErrRecMgr_OutercodeData_ErasedPageOffset.GetName( ), '=', ErrRecMgr_OutercodeData_ErasedPageOffset.GetValue( )
      ErrRecMgr_OutercodeData_Lba = ErrRecMgr_OutercodeData.GetChildMemberWithName( "Lba" )
      print '   ', ErrRecMgr_OutercodeData_Lba.GetName( ), '=', ErrRecMgr_OutercodeData_Lba.GetValue( )
      ErrRecMgr_OutercodeData_BlockId = ErrRecMgr_OutercodeData.GetChildMemberWithName( "BlockId" )
      print '   ', ErrRecMgr_OutercodeData_BlockId.GetName( ), '=', ErrRecMgr_OutercodeData_BlockId.GetValue( )
      ErrRecMgr_OutercodeData_ParityBuffer = ErrRecMgr_OutercodeData.GetChildMemberWithName( "ParityBuffer" )
      print '   ', ErrRecMgr_OutercodeData_ParityBuffer.GetName( ), '=', ErrRecMgr_OutercodeData_ParityBuffer.GetValue( )
      ErrRecMgr_OutercodeData_NumParitiesWritten = ErrRecMgr_OutercodeData.GetChildMemberWithName( "NumParitiesWritten" )
      print '   ', ErrRecMgr_OutercodeData_NumParitiesWritten.GetName( ), '=', ErrRecMgr_OutercodeData_NumParitiesWritten.GetValue( )
      ErrRecMgr_OutercodeData_NumParitiesProcessed = ErrRecMgr_OutercodeData.GetChildMemberWithName( "NumParitiesProcessed" )
      print '   ', ErrRecMgr_OutercodeData_NumParitiesProcessed.GetName( ), '=', ErrRecMgr_OutercodeData_NumParitiesProcessed.GetValue( )
      ErrRecMgr_OutercodeData_CorruptedOrGeneratedMaskIsSet = ErrRecMgr_OutercodeData.GetChildMemberWithName( "CorruptedOrGeneratedMaskIsSet" )
      print '   ', ErrRecMgr_OutercodeData_CorruptedOrGeneratedMaskIsSet.GetName( ), '=', ErrRecMgr_OutercodeData_CorruptedOrGeneratedMaskIsSet.GetValue( )
      ErrRecMgr_OutercodeData_XorHeader = ErrRecMgr_OutercodeData.GetChildMemberWithName( "XorHeader" )
      print '   ', ErrRecMgr_OutercodeData_XorHeader


   def __init__(self ):
      target = lldb.debugger.GetSelectedTarget( )

      ErrRecMgr = target.FindFirstGlobalVariable( "ErrorRecoveryMgr" )
 
      self.printNicely( ErrRecMgr )

class VbmBufferMgrPrint( ):

   def printNicely( self ):
      target = lldb.debugger.GetSelectedTarget( )
      VbmBufferMgr = target.FindFirstGlobalVariable( "VbmBufferMgr" )
      VbmBufferMgrEntry = target.FindFirstType( "vbm_buffer_mgr_entry" )
      BufferAddress = 0

      ################################################################################
      #                        OUTPUT
      ################################################################################
      print VbmBufferMgr.GetType( )

      Entry_Addr = VbmBufferMgr.GetChildMemberWithName( 'Sentinel' ).GetChildMemberWithName( 'Next' ).GetValueAsUnsigned( )
      LastElementAddr = VbmBufferMgr.GetChildMemberWithName( 'Sentinel' ).GetChildMemberWithName( 'Previous' ).GetValueAsUnsigned( )

      while True:
         addr = lldb.SBAddress( Entry_Addr, lldb.target )
         Entry = target.CreateValueFromAddress( "vbm_buffer_mgr_entry *", addr, VbmBufferMgrEntry )
         Entry_Addr = Entry.GetChildMemberWithName( 'Link' ).GetChildMemberWithName( 'Next' ).GetValueAsUnsigned( )
         if BufferAddress == 0:
            BufferAddress = Entry.GetChildMemberWithName( 'BufferPtr' ).GetValue( )
         print 'VbmIndex:', Entry.GetChildMemberWithName( 'VbmIndex' ).GetValue( ), ' @', Entry.GetChildMemberWithName( 'BufferPtr' ).GetValue()
         if LastElementAddr == Entry_Addr:
            break

      mem_read_string = "memory read -s1 -l32 -fx -c0x1100 --force " + BufferAddress
      lldb.debugger.HandleCommand( mem_read_string )

   def __init__(self ):
      self.printNicely( )


def WalkLinksAtSentinel( start, link_type, function = None ):
    '''
    This function takes two arguments
    start is address of stx link sentinel to start walking from
    link_type is either stx_single_link_sentinel or stx_double_link
    function is optional parameter. function() will be called for each element
    '''
    target = lldb.debugger.GetSelectedTarget( )
    Sentinel = target.FindFirstType( link_type )

    link_type += '*'

    loop = 0
    filtered_matches = 0
    ptr_next = int( start, 0 )
    if ptr_next == 0:
       return 0

    sb_addr = lldb.SBAddress( ptr_next, lldb.target )
    Sentinel_ptr = target.CreateValueFromAddress( link_type, sb_addr, Sentinel )
    ptr_previous = Sentinel_ptr.GetChildMemberWithName( "Previous" ).GetValueAsUnsigned( )
    ptr_next = Sentinel_ptr.GetChildMemberWithName( "Next" ).GetValueAsUnsigned( )

    while True:
       next_addr = lldb.SBAddress( ptr_next, lldb.target )
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


def ParseAndPrintFMR( command_args ):
   description='''Use this to print flash_media_req struct'''

   def ParseOptions(command_name, description ):
      usage = "usage: %prog [options] <FILE> [FILE ...]"
      option_parser = optparse.OptionParser(description=description, prog='crashlog',usage=usage)
      option_parser.add_option('--verbose'       , '-v', action='store_true', dest='verbose', help='display verbose debug info', default=False)
      return option_parser

   option_parser = ParseOptions( 'print fmr', description )

   try:
      (options, args) = option_parser.parse_args(command_args)
   except:
      print 'my custom exception'
      return

   if args:
      for address in args:
          FmrPrint( address )

def ParseAndPrintRH( command_args ):
   description='''Use this to print flash_media_req_handle struct'''

   def ParseOptions(command_name, description ):
      usage = "usage: %prog [options] <FILE> [FILE ...]"
      option_parser = optparse.OptionParser(description=description, prog='crashlog',usage=usage)
      option_parser.add_option('--verbose'       , '-v', action='store_true', dest='verbose', help='display verbose debug info', default=False)
      return option_parser

   option_parser = ParseOptions( 'print rh', description )

   try:
      (options, args) = option_parser.parse_args(command_args)
   except:
      print 'my custom exception'
      return

   if args:
      for address in args:
          ReqHandlePrint( address )

def pfmr( debugger, command, result, dict ):
   try:
       ParseAndPrintFMR( shlex.split( command ) )
   except:
       result.PutCString ("error: python exception %s" % sys.exc_info()[0])

def prh( debugger, command, result, dict ):
   try:
       ParseAndPrintRH( shlex.split( command ) )
   except:
       result.PutCString ("error: python exception %s" % sys.exc_info()[0])


if __name__ == '__main__':
   # Create a new debugger instance
   #lldb.debugger = lldb.SBDebugger.Create()
   print "It's not expected to be executed. Only imported"
elif getattr(lldb, 'debugger', None):
   lldb.debugger.HandleCommand('command script add -f ssd_prints.pfmr pfmr')
   lldb.debugger.HandleCommand('command script add -f ssd_prints.prh prh')

   print '"pfmr", "prh" commands are installed'


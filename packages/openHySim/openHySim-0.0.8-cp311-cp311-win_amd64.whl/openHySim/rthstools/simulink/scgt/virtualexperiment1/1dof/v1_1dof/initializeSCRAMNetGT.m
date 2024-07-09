%INITIALIZESCRAMNETGT to initialize the parameters needed for SCRAMNet GT
%
% created by Brad Thoen (MTS)
% modified by Andreas Schellenberg (andreas.schellenberg@gmail.com) 01/2014

%%%%%%%%%% SIGNAL COUNTS %%%%%%%%%%


%%%%%%%%%% SCRAMNET PARTITIONS %%%%%%%%%%

opfNode  = 10;   % OpenFresco node
xpcNode	 = 20;   % xPC-Target node
syncNode = 30;   % synchronization node: MTS FlexTest

%%%%%%%%%% START MTS (FlexTest) %%%%%%%%%%

%%%%%%%%%% outputs to FlexTest from Speedgoat %%%%%%%%%%


outpartition = scgtpartitionstruct([]);
% Disp1 Partition
outpartition(1).Address = '0x0';
outpartition(1).Type = 'double';
outpartition(1).Size = '1';
% Disp2 Partition
outpartition(2).Address = '0x8';
outpartition(2).Type = 'double';
outpartition(2).Size = '1';



%%%%%%%%%% inputs from FlexTest to xPC %%%%%%%%%%

inppartition = scgtpartitionstruct([]);
% Disp1 fbk Partition
inppartition(1).Address = '0x100';
inppartition(1).Type = 'double';
inppartition(1).Size = '1';
% Disp2 fbk Partition
inppartition(2).Address = '0x108';
inppartition(2).Type = 'double';
inppartition(2).Size = '1';
% Force1 fbk Partition
inppartition(3).Address = '0x110';
inppartition(3).Type = 'double';
inppartition(3).Size = '1';
% Force2 fbk Partition
inppartition(4).Address = '0x118';
inppartition(4).Type = 'double';
inppartition(4).Size = '1';

%%%%%%%%%% END MTS (FlexTest) %%%%%%%%%%


%%%%%%%%%% START OPENFRESCO %%%%%%%%%%

%%%%%%%%%% inputs from OpenFresco to xPC %%%%%%%%%%

% newTarget (from)
baseAddress = 1024;
opfpartition(1).Address = ['0x', dec2hex(baseAddress*4)];
opfpartition(1).Type = 'int32';
opfpartition(1).Size = '1';

% control signals (from)
opfpartition(2).Type = 'single';
opfpartition(2).Size = num2str(nDOF);

%%%%%%%%%% outputs to OpenFresco from xPC %%%%%%%%%%

% switchPC (to)
opfpartition(3).Type = 'int32';
opfpartition(3).Size = '1';

% atTarget (to)
opfpartition(4).Type = 'int32';
opfpartition(4).Size = '1';

% daq signals (to)
opfpartition(5).Type = 'single';
opfpartition(5).Size = num2str(2*nDOF);

%%%%%%%%%% END OPENFRESCO %%%%%%%%%%


%%%%%%%%%% scramnet node configuration %%%%%%%%%%

mask = sprintf('0x%8.8X', bitshift(1, syncNode));
node = scgtnodestruct([]);
node.Interface.NodeID                                  = num2str(xpcNode);
node.Interface.Interrupts.ChangeBroadcastInterruptMask = 'yes';
node.Interface.Interrupts.BroadcastInterruptMask       = mask;
outpartition    = scgtpartitionstruct(outpartition);
inppartition    = scgtpartitionstruct(inppartition);
opfpartition    = scgtpartitionstruct(opfpartition);
node.Partitions = [outpartition inppartition opfpartition];
node            = scgtnodestruct(node);

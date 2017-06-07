! Setup
int fie set fie = .gui.msg_box.message act = append str = '', 'Reading  %(path)s/PatientData.csv..'
int fie set fie = dbox_runModel.field_fileName str =  '%(path)s/PatientData.csv'

!int tog mod tog=.OCDL.dbox_runModel.toggle_advanced state=on			! no static images
!int tog mod tog=.OCDL.dbox_runModel.toggle_onlySim state=on			!

!int tog mod tog=.OCDL.dbox_runModel.toggle_advanced state=on			!
!int tog mod tog=.OCDL.dbox_runModel.toggle_onlyImg state=on			! only static images
!int tog mod tog=.OCDL.dbox_runModel.toggle_onlySim state=off			!

if c=%(run_cp)s
! CP Export
int pus exe pus = .OCDL.dbox_runModel.toggle_compPlace
int fie set fie = .gui.msg_box.message act = append str = '', 'Exporting %(path)s/PatientData.csv..'
int fie set fie = dbox_compplacement.field_fileName str = '%(path)s/ComponentPlacement.csv'
int pus exe pus = dbox_compplacement.button_export
end

if c= %(run_single)s
! Single Run
int fie set fie = .gui.msg_box.message act = append str = '', 'Running  %(path)s/PatientData.csv..'
int tog mod tog=.OCDL.dbox_runModel.toggle_RandD state=off
var set var = .gui.fOut str = 'ready_to_run.command'
file text open  file = (eval(.gui.fOut )) open_mode = overwrite
file text write file = (eval(.gui.fOut )) format = ''
file text close file = (eval(.gui.fOut ))
int pus exe pus = .OCDL.dbox_runModel.button_apply
end

if c=%(run_doe)s
! Beta(DoE)
int fie set fie = .gui.msg_box.message act = append str = '', 'Running Beta %(path)s/PatientData.csv..'
int tog mod tog=.OCDL.dbox_runModel.toggle_RandD state=on
int pus exe pus = .OCDL.dbox_runModel.button_apply
end

quit
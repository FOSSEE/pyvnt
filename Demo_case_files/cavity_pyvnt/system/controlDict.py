from pyvnt import *

controlDict = Node_C("controlDict")

app = Key_C("application", Enm_P("application", {"icoFoam", "simpleFoam", "pimpleFoam"}, "icoFoam"))

controlDict.add_data(app)

startFrom = Key_C("startFrom", Enm_P("startFrom", {"startTime", "latestTime"}, "startTime"))

controlDict.add_data(startFrom)

startTime = Key_C("startTime", Flt_P("startTime", 0))

controlDict.add_data(startTime)

stopAt = Key_C("stopAt", Enm_P("stopAt", {"endTime", "startTime"}, "endTime"))

controlDict.add_data(stopAt)

endTime = Key_C("endTime", Flt_P("endTime", 0.5))

controlDict.add_data(endTime)

deltaT = Key_C("deltaT", Flt_P("deltaT", 0.005))

controlDict.add_data(deltaT)

writeControl = Key_C("writeControl", Enm_P("writeControl", {"timeStep", "runTime", "adjustableRunTime"}, "timeStep"))

controlDict.add_data(writeControl)

writeInterval = Key_C("writeInterval", Int_P("writeInterval", 20))

controlDict.add_data(writeInterval)

purgeWrite = Key_C("purgeWrite", Flt_P("purgeWrite", 0))

controlDict.add_data(purgeWrite)

writeFormat = Key_C("writeFormat", Enm_P("writeFormat", {"ascii", "binary"}, "ascii"))

controlDict.add_data(writeFormat)

writePrecision = Key_C("writePrecision", Int_P("writePrecision", 6))

controlDict.add_data(writePrecision)

writeCompression = Key_C("writeCompression", Enm_P("writeCompression", {"off", "on"}, "off"))

controlDict.add_data(writeCompression)

timeFormat = Key_C("timeFormat", Enm_P("timeFormat", {"general", "scientific"}, "general"))

controlDict.add_data(timeFormat)

timePrecision = Key_C("timePrecision", Int_P("timePrecision", 6))

controlDict.add_data(timePrecision)

runTimeModifiable = Key_C("runTimeModifiable", Enm_P("runTimeModifiable", {"true", "false"}, "true"))

controlDict.add_data(runTimeModifiable)

writeTo(controlDict, "Demo_case_files/")
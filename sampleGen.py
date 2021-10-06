import UniversalClasses as uc
import SaveFile
import detGen
import oneSidedGen
import nonDetGen

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"
grey = "9EA9A4"
light_blue = "C2DCFE"

if __name__ == "__main__":
    # Sample determinsitic systems
    sys1 = detGen.genDoubleIndexStates(9)
    SaveFile.main(sys1, ["XML Files/samples/smallIndexStatesDet.xml"])

    sys2 = detGen.genDoubleIndexStates(100)
    SaveFile.main(sys2, ["XML Files/samples/largeIndexStatesDet.xml"])

    sys3 = detGen.genSqrtBinString("110011010")
    SaveFile.main(sys3, ["XML Files/samples/smallBinStringDet.xml"])

    sys4 = detGen.genSqrtBinString("1100110101101010101100110")
    SaveFile.main(sys4, ["XML Files/samples/largeBinStringDet.xml"])

    sys5 = detGen.genSqrtBinCount(50)
    SaveFile.main(sys5, ["XML Files/samples/smallBinCountDet.xml"])

    sys6 = detGen.genSqrtBinString(125)
    SaveFile.main(sys6, ["XML Files/samples/largeBinCountDet.xml"])

    sys7 = detGen.genSqrtBaseBString("123456789", 10)
    SaveFile.main(sys7, ["XML Files/samples/smallDecimalStringDet.xml"])

    sys8 = detGen.genSqrtBaseBString("123456789012345", 10)
    SaveFile.main(sys8, ["XML Files/samples/largeDecimalStringDet.xml"])

    sys9 = detGen.genSqrtBaseBCount("9950", 10)
    SaveFile.main(sys9, ["XML Files/samples/smallBinCountDet.xml"])

    sys10 = detGen.genSqrtBaseBString("999999000", 10)
    SaveFile.main(sys10, ["XML Files/samples/largeBinCountDet.xml"])

    # Sample One Sided systems
    sys11 = oneSidedGen.genTripleIndexStates(27)
    SaveFile.main(sys11, ["XML Files/samples/smallIndexStates1S.xml"])

    sys12 = oneSidedGen.genTripleIndexStates(125)
    SaveFile.main(sys12, ["XML Files/samples/largeIndexStates1S.xml"])

    sys13 = oneSidedGen.cbrtBinString("110011010110011010110011010")
    SaveFile.main(sys13, ["XML Files/samples/BinString1S.xml"])

    sys14 = oneSidedGen.genSqrtBinCount(1000)
    SaveFile.main(sys14, ["XML Files/samples/smallBinCount1S.xml"])

    # Sample General systems
    sys15 = nonDetGen.genQuadIndexStates(81)
    SaveFile.main(sys11, ["XML Files/samples/IndexStatesND.xml"])

    num = ""

    for i in range(27):
        num += "101"

    sys16 = nonDetGen.genQuadBinString(num)
    SaveFile.main(sys16, ["XML Files/samples/BinStringND.xml"])

    sys16 = nonDetGen.quadBinCount(1500)
    SaveFile.main(sys16, ["XML Files/samples/BinCountND.xml"])
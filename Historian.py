import json

from UniversalClasses import Assembly, State, Tile

from PyQt5.QtWidgets import QFileDialog

class Historian:

    class Assemblies:
        def __init__(self, movelist, assembly):
            self.movelist = movelist
            self.assembly = assembly

    def __init__(self):
        pass

    def set_ui_parent(self, ui):
        self.ui = ui

    def set_engine(self, engine):
        self.engine = engine
    
    def dump(self):
        filename = QFileDialog.getSaveFileName(self.ui, "Assembly JSON File", "", "JSON Files (*.json)")

        if filename[0] != '':
            fp = open(filename[0], 'w')
            assemblies = self.Assemblies(self.engine.moveList, self.engine.currentAssembly)
            # Dumping into one line saves a ton of space, but becomes completly unreadable, worse than it already is
            # json.dump(assemblies, fp, sort_keys=False, default=self.encoder)
            # Dumping with some indentation makes it nice-ish, but takes a large amount of space for \n and \t and ' '
            json.dump(assemblies, fp, sort_keys=False, default=self.encoder, indent=2)

    def dumps(self):
        print("Dumping Assemblies")
        assemblies = self.Assemblies(self.engine.moveList, self.engine.currentAssembly)
        print(json.dumps(assemblies, sort_keys=False, default=self.encoder, indent=2))
    
    def load(self):
        filename = QFileDialog.getOpenFileName(self.ui, "Select JSON History", "", "JSON Files (*.json)")

        if filename[0] != "":
            fp = open(filename[0], 'r')

            assemblies = json.load(fp)
        
        print(assemblies)

        # Break down the history
        movelist = assemblies["history"]

        # Break down the assembly
        assembly = assemblies["assembly"]

    def loads(self):
        print("Loading Assembiles")
        moveHistoryEncoded = json.dumps(self.engine.moveList, sort_keys=False, default=self.encoder, indent=3)
        moveHistoryDecoded = json.loads(moveHistoryEncoded)

        print("History decoded into...")
        print(*moveHistoryDecoded)

        # Convert moveHistoryDecoded from dictionary to actual object it represents (state dictionary into state object)

        eq = moveHistoryEncoded == json.dumps(moveHistoryDecoded, sort_keys=False, default=self.encoder, indent=3)

        if eq:
            print("Strings are the same! History Decode PASS")
        else:
            print("String are NOT the same! History Decode FAIL")
        
        assemblyEncoded = json.dumps(self.engine.currentAssembly, sort_keys=False, default=self.encoder, indent=3)
        assemblyDecoded = json.loads(assemblyEncoded)

        print("Assembly decoded into...")
        print(*assemblyDecoded)

        # Convert assemblyDecoded into actual objects

        eq = assemblyEncoded == json.dumps(assemblyDecoded, sort_keys=False, default=self.encoder, indent=3)

        if eq:
            print("Strings are the same! Assembly Decode PASS")
        else:
            print("String are NOT the same! Assembly Decode FAIL")

    def encoder(self, obj):
        # what state should look like in json
        if isinstance(obj, State):
            return obj.get_label()
        elif isinstance(obj, self.Assemblies):
            dict = {}
            dict["history"] = obj.movelist
            dict["assembly"] = obj.assembly

            return dict
        elif isinstance(obj, Tile):
            tiledict = {}
            tiledict["state"] = obj.state
            tiledict["x"] = obj.x
            tiledict["y"] = obj.y

            return tiledict
        elif isinstance(obj, Assembly):
            # create dictionary from the instance variables
            assemblydict = {}

            assemblydict["label"] = obj.label
            assemblydict["tiles"] = obj.tiles
            assemblydict["coords"] = obj.coords
            assemblydict["leftMost"] = obj.leftMost
            assemblydict["rightMost"] = obj.rightMost
            assemblydict["upMost"] = obj.upMost
            assemblydict["downMost"] = obj.downMost

            return assemblydict

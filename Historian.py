import json

from UniversalClasses import Assembly, State, Tile

class Historian:

    def __init__(self):
        pass

    def set_engine(self, engine):
        self.engine = engine

    def dumps(self):
        print("Dumping Assemblies")
        print("Move History")
        print(json.dumps(self.engine.moveList, sort_keys=False, default=self.encoder, indent=3))
        print("Current Assembly")
        print(json.dumps(self.engine.currentAssembly, sort_keys=False, default=self.encoder, indent=3))
    
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

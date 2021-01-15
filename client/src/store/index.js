import _ from "lodash";
import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

const defaultAnnotations = {
  file_attributes: {},
  regions: []
};

const defaultState = {
  projectName: "",
  projectFiles: [],
  projectSettings: {},
  connectionName: "",
  currentFileIndex: -1,
  currentSelectionIndex: -1,
  currentAnnotations: _.cloneDeep(defaultAnnotations),
  coloringAttribute: null,
  currentDefaults: {},
  colorMap: {},
  isEditing: false
};

// https://www.w3schools.com/colors/colors_hex.asp
// blue, deep-sky-blue, medium-spring-green, aqua, cyan, royal-blue, indigo, slate-blue, purple, dark-red, orchid, gold, yellow, khaki, olive, sandy-brown
const COLORS = [
  "#0000FF",
  "#00BFFF",
  "#00FA9A",
  "#00FFFF",
  "#00FFFF",
  "#4169E1",
  "#4B0082",
  "#6A5ACD",
  "#800080",
  "#8B0000",
  "#DA70D6",
  "#FFD700",
  "#FFFF00",
  "#BDB76B",
  "#808000",
  "#F4A460"
];

export default createStore({
  state: _.cloneDeep(defaultState),

  getters: {
    getCurrentFileName(state) {
      return state.projectFiles[state.currentFileIndex];
    },

    getNumFiles(state) {
      return state.projectFiles.length;
    },

    getRegions: state => () => {
      // console.log("regions", JSON.stringify(state.currentAnnotations.regions));
      return state.currentAnnotations.regions;
    },

    getAttributeNames: state => () => {
      return Object.keys(state.projectSettings.attributes);
    },

    getAttributeType: state => name => {
      // console.log("checking for", name);
      return state.projectSettings.attributes[name].type;
    },

    getAttributeValues: state => name => {
      return state.projectSettings.attributes[name].values;
    },

    getDefaultValue: state => name => {
      return state.currentDefaults[name];
    },

    getCondition: state => name => {
      return state.projectSettings.attributes[name].condition;
    },

    getSelectionValue: (state, getters) => name => {
      let res;
      if (state.currentSelectionIndex > -1) {
        res = state.currentAnnotations.regions[state.currentSelectionIndex].attributes[name];
      }
      res = res ?? getters.getIndeterminateValue(name);
      return res;
    },

    getIndeterminateValue: state => name => {
      let res;
      switch (state.projectSettings.attributes[name].type) {
        case "radio": {
          res = null;
          break;
        }
        case "checkbox": {
          res = [];
          break;
        }
        case "text": {
          res = "";
          break;
        }
        default:
          res = "";
      }
      return res;
    },

    getSelectionPoints: state => () => {
      let res = [0, 0, 0, 0];
      if (state.currentSelectionIndex > -1) {
        res = state.currentAnnotations.regions[state.currentSelectionIndex].points;
      }
      // console.log("selection points", JSON.stringify(res));
      return res;
    },

    getRadioAttributeNames: state => () => {
      return Object.keys(
        _.pickBy(state.projectSettings.attributes, function f(o) {
          return o.type === "radio";
        })
      );
    },

    getCurrentRegionColor: state => () => {
      if (state.coloringAttribute) {
        return state.colorMap[state.currentDefaults[state.coloringAttribute]];
      }
      return "#000000";
    },

    getRegionValueColor: state => value => {
      if (state.coloringAttribute) {
        return state.colorMap[value];
      }
      return "#000000";
    }
  },

  mutations: {
    reset(state) {
      Object.keys(state).forEach(key => {
        state[key] = defaultState[key];
      });
    },

    updateAttribute(state, update) {
      state.projectSettings.attributes[update.name] = {
        type: update.type,
        values: update.values,
        condition: update.condition
      };
      [state.currentDefaults[update.name]] = update.values;
    },

    addBox(state, bbox) {
      const region = {
        attributes: _.cloneDeep(state.currentDefaults),
        points: bbox,
        shape: "rect"
      };
      state.currentAnnotations.regions.push(region);
    },

    setProjectFiles(state, files) {
      state.projectFiles = files;
    },

    setProjectSettings(state, settings) {
      state.projectSettings = settings;
      state.currentDefaults = _.mapValues(state.projectSettings.attributes, function f(o) {
        let setter;
        switch (o.type) {
          case "radio":
            setter = null;
            break;
          case "checkbox":
            setter = [];
            break;
          case "text":
            setter = "";
            break;
          default:
            break;
        }
        return setter;
      });
    },

    setDefaultAttribute(state, keyValue) {
      switch (state.projectSettings.attributes[keyValue.key].type) {
        case "radio":
          state.currentDefaults[keyValue.key] = keyValue.value;
          break;
        case "checkbox": {
          const idx = state.currentDefaults[keyValue.key].indexOf(keyValue.value);
          if (idx > -1) {
            state.currentDefaults[keyValue.key].splice(idx, 1);
          } else {
            state.currentDefaults[keyValue.key].push(keyValue.value);
          }
          break;
        }
        case "text":
          state.currentDefaults[keyValue.key] = keyValue.value;
          break;
        default:
          // console.log("type not found");
          break;
      }
      // console.log("current defaults", JSON.stringify(state.currentDefaults));
    },

    setSelectionAttribute(state, keyValue) {
      if (state.currentSelectionIndex > -1) {
        if (
          !(
            keyValue.key in state.currentAnnotations.regions[state.currentSelectionIndex].attributes
          )
        ) {
          let res;
          switch (state.projectSettings.attributes[keyValue.key].type) {
            case "radio": {
              res = null;
              break;
            }
            case "checkbox": {
              res = [];
              break;
            }
            case "text": {
              res = "";
              break;
            }
            default:
              res = "";
          }
          state.currentAnnotations.regions[state.currentSelectionIndex].attributes[
            keyValue.key
          ] = res;
        }
        switch (state.projectSettings.attributes[keyValue.key].type) {
          case "radio":
            state.currentAnnotations.regions[state.currentSelectionIndex].attributes[keyValue.key] =
              keyValue.value;
            break;
          case "checkbox": {
            const idx = state.currentAnnotations.regions[state.currentSelectionIndex].attributes[
              keyValue.key
            ].indexOf(keyValue.value);
            if (idx > -1) {
              state.currentAnnotations.regions[state.currentSelectionIndex].attributes[
                keyValue.key
              ].splice(idx, 1);
            } else {
              state.currentAnnotations.regions[state.currentSelectionIndex].attributes[
                keyValue.key
              ].push(keyValue.value);
            }
            break;
          }
          case "text":
            state.currentAnnotations.regions[state.currentSelectionIndex].attributes[keyValue.key] =
              keyValue.value;
            break;
          default:
            // console.log("selection type not found");
            break;
        }
        // console.log(
        //   "current selection attributes",
        //   JSON.stringify(
        //     state.currentAnnotations.regions[state.currentSelectionIndex].attributes[keyValue.key]
        //   )
        // );
      }
    },

    setConnectionName(state, name) {
      state.connectionName = name;
    },

    setProjectName(state, name) {
      state.projectName = name;
    },

    setCurrentFileIndex(state, filename) {
      state.currentFileIndex = state.projectFiles.findIndex(fname => fname === filename);
      state.currentAnnotations = _.cloneDeep(defaultAnnotations);
    },

    setCurrentAnnotations(state, anns) {
      // console.log("received anns", JSON.stringify(anns));
      if (Object.keys(anns).length > 0) {
        state.currentAnnotations = anns;
      }
    },

    goPrevious(state) {
      state.currentFileIndex -= 1;
      state.currentSelectionIndex = -1;
      state.currentAnnotations = _.cloneDeep(defaultAnnotations);
    },

    goNext(state) {
      state.currentFileIndex += 1;
      state.currentSelectionIndex = -1;
      state.currentAnnotations = _.cloneDeep(defaultAnnotations);
    },

    removeBox(state, boxIdx) {
      if (boxIdx > -1) {
        state.currentAnnotations.regions.splice(boxIdx, 1);
        state.currentSelectionIndex = -1;
      }
    },

    setSelectedBox(state, bbox) {
      if (bbox) {
        state.currentSelectionIndex = state.currentAnnotations.regions.findIndex(region => {
          return (
            region.points[0] === bbox[0] &&
            region.points[1] === bbox[1] &&
            region.points[2] === bbox[2] &&
            region.points[3] === bbox[3]
          );
        });
      } else {
        state.currentSelectionIndex = -1;
      }
      // console.log("current selection", state.currentSelectionIndex);
    },

    setColoringAttribute(state, name) {
      state.colorMap = {};
      state.coloringAttribute = name;
      if (name) {
        state.projectSettings.attributes[name].values.forEach(function f(item, idx) {
          state.colorMap[idx] = COLORS[idx];
        });
      }
    },

    toggleEditing(state) {
      state.isEditing = !state.isEditing;
      // console.log("editing", state.isEditing);
    }
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState()]
});

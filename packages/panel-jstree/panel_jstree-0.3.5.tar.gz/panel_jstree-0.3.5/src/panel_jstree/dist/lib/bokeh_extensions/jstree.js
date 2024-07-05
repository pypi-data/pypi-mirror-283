var _a;
import { div } from "@bokehjs/core/dom";
import { HTMLBox, HTMLBoxView, set_size } from "./layout";
function ID() {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substring(2, 11);
}
export class jsTreePlotView extends HTMLBoxView {
    initialize() {
        super.initialize();
        this._last_selected = [];
    }
    connect_signals() {
        // console.log("connect")
        super.connect_signals();
        this.connect(this.model.properties._data.change, () => this._update_tree_from_data());
        this.connect(this.model.properties.value.change, () => this._update_selection_from_value());
        this.connect(this.model.properties._new_nodes.change, () => this._update_tree_from_new_nodes());
        this.connect(this.model.properties.checkbox.change, () => this.setCheckboxes());
        this.connect(this.model.properties.show_icons.change, () => this._setShowIcons());
        this.connect(this.model.properties.show_dots.change, () => this._setShowDots());
        this.connect(this.model.properties.multiple.change, () => this._setMultiple());
        // console.log(this.model.show_dots)
        // console.log(this.model.show_icons)
    }
    render() {
        super.render();
        this._id = ID();
        // console.log(this._id)
        this._container = div({ id: this._id, style: "overflow: auto; minHeight: 200px; minWidth: 200px;" });
        set_size(this._container, this.model);
        this.shadow_el.appendChild(this._container);
        // console.log(this._container)
        if (this.model.checkbox && !this.model.plugins.includes("checkbox")) {
            this.model.plugins.push("checkbox");
        }
        this._jstree = jQuery(this._container).jstree({ "core": { "data": this.model._data, "check_callback": true,
                "multiple": this.model.multiple,
                "themes": {
                    "dots": this.model.show_dots,
                    "icons": this.model.show_icons
                }
            },
            "plugins": this.model.plugins,
            checkbox: {
                three_state: this.model.cascade_setting == "" ? this.model.cascade : false,
                cascade: this.model.cascade_setting == "" ? "up+down+undetermined" : this.model.cascade_setting,
                cascade_to_disabled: false,
            }
        });
        this.init_callbacks();
    }
    init_callbacks() {
        // Initialization
        // Rendering callbacks
        // TODO: do I need both of these?
        this._jstree.on('refresh.jstree', ({}, {}) => this._update_selection_from_value());
        // Sync state with model
        this._jstree.on('model.jstree', ({}, {}) => this.onNewData());
        this._jstree.on('activate_node.jstree', ({}, data) => this.selectNodeFromEditor({}, data));
        this._jstree.on('before_open.jstree', (e, data) => this._listen_for_node_open(e, data));
    }
    onNewData() {
        this.model._flat_tree = this._jstree.jstree(true).get_json(null, { "flat": true });
        // console.log("Flat tree: ", this.model._flat_tree)
    }
    selectNodeFromEditor({}, data) {
        // console.log("select pre", this.model.value)
        this.model.value = data.instance.get_selected();
        // console.log("select post", this.model.value)
    }
    _update_selection_from_value() {
        // console.log("update selection from value")
        this._jstree.jstree(true).select_node(this.model.value);
        // We sometimes have to fire this function more than once per value change because of
        // calling jstree.refresh, so we check to see if model.value has really changed
        // by comparing to last_selected
        if (this.model.value != this._last_selected) {
            let deselected = this._last_selected.filter(x => !this.model.value.includes(x));
            this._jstree.jstree(true).deselect_node(deselected);
        }
        // We choose get_selected
        this._last_selected = this.model.value;
    }
    _update_tree_from_new_nodes() {
        // console.log("new nodes: ", this.model._new_nodes)
        for (let node of this.model._new_nodes) {
            this._jstree.jstree(true).create_node(node["parent"], node, "first");
        }
        this._jstree.jstree(true).settings.core.data = this._jstree.jstree(true).get_json(null, { no_li_attr: true, no_a_attr: true, no_data: true });
        this.model._data = this._jstree.jstree(true).settings.core.data;
        // this._update_selection_from_value()
    }
    _update_tree_from_data() {
        // console.log("updating data")
        this._jstree.jstree(true).settings.core.data = this.model._data;
        // console.log("data: ", this._jstree.jstree(true).settings.core.data)
        // console.log("value after data", this.model.value)
        // This will redraw the tree if we swap out the data with new data
        // we set forget_state to true, so the current state is not reapplied
        // letting whatever state is set in the new data (open or closed, etc)
        // be the new state
        this._jstree.jstree(true).refresh({ "skip_loading": false,
            "forget_state": true });
        // selected state is not preserved correctly right now, so we then
        // deselect everything because that is better than getting it wrong
        this._jstree.jstree(true).deselect_all({ "supress_event": true });
        // console.log("value after refresh", this.model.value)
        // console.log("data after refresh", this._jstree.jstree(true).settings.core.data)
    }
    _setShowIcons() {
        // console.log("setShowIcons")
        if (this.model.show_icons) {
            this._jstree.jstree(true).show_icons();
        }
        else {
            this._jstree.jstree(true).hide_icons();
        }
    }
    _setShowDots() {
        // console.log("setShowDots")
        if (this.model.show_dots) {
            this._jstree.jstree(true).show_dots();
        }
        else {
            this._jstree.jstree(true).hide_dots();
        }
    }
    setCheckboxes() {
        // console.log("setCheckBoxes")
        if (this.model.checkbox) {
            this._jstree.jstree(true).show_checkboxes();
        }
        else {
            this._jstree.jstree(true).hide_checkboxes();
        }
    }
    _setMultiple() {
        // console.log("setMultiple")
        this._jstree.jstree(true).settings.core.multiple = this.model.multiple;
    }
    _update_tree_theme_from_model() {
        this._jstree.jstree(true).refresh(false, true);
    }
    _listen_for_node_open({}, data) {
        // console.log("listen for node open")
        data.node = this.add_node_children(data.node);
        this.model._last_opened = data.node;
    }
    add_node_children(node) {
        // console.log("add node children")
        node["children_nodes"] = [];
        for (let child of node.children) {
            node.children_nodes.push(this._jstree.jstree(true).get_node(child));
        }
        return node;
    }
}
jsTreePlotView.__name__ = "jsTreePlotView";
export class jsTreePlot extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
}
_a = jsTreePlot;
jsTreePlot.__name__ = "jsTreePlot";
jsTreePlot.__module__ = "panel_jstree.bokeh_extensions.jstree";
(() => {
    _a.prototype.default_view = jsTreePlotView;
    _a.define(({ Array, Any, Boolean }) => ({
        value: [Array(Any), []],
        _data: [Array(Any), []],
        plugins: [Array(Any), []],
        checkbox: [Boolean, true],
        multiple: [Boolean, true],
        show_icons: [Boolean, true],
        show_dots: [Boolean, true],
        cascade: [Boolean, true],
        cascade_setting: [Any, ""],
        _last_opened: [Any, {}],
        _new_nodes: [Array(Any), []],
        _flat_tree: [Array(Any), []],
    }));
})();
//# sourceMappingURL=jstree.js.map
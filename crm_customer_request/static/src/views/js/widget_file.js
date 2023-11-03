/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class MyNewWidget extends Component {
    setup() {
        // initialize component here
        super.setup();
    }
}

MyNewWidget.template = "crm_customer_request.MyNewWidget";

MyNewWidget.defaultProps = {
    backgroundColor: "primary",
}
// Spread standard field props and add custom props
MyNewWidget.props = {
    ...standardFieldProps,
    placeholder: {type: String, optional: true},
    backgroundColor: {type: String, optional: true},
};

MyNewWidget.extractProps = ({attrs,field}) => {
    return {
        placeholder: attrs.placeholder,
        backgroundColor: attrs.background_color,
    };
};

MyNewWidget.supportedTypes = ["float", "int"];

// Add field to correct category
registry.category("field").add("new_widget", MyNewWidget);
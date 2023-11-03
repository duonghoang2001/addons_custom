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

MyNewWidget.props = {
    ...standardFieldProps,
    placeholder: { type: String, optional: true },
};

MyNewWidget.extractProps = ({attrs}) => {
    return {
        placeholder: attrs.placeholder,
    };
};

//MyNewWidget.displayName = _lt("My Widget");

MyNewWidget.supportedTypes = ["float", "int"];
registry.category("field").add("new_widget", MyNewWidget);
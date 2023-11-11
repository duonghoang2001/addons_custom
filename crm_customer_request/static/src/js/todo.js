/** @odoo-module */

import { Component } from "@odoo/owl";

export class Todo extends Component {
    onClick(ev) {
        this.props.toggleState(this.props.id);
    }

    onRemove() {
        this.props.removeTodo(this.props.id);
    }
}

Todo.template = "crm_customer_request.Todo";

Todo.props = {
    id : { type: Number },
    description : { type: String },
    done : { type: Boolean },
    toggleState : { type: Function },
    removeTodo : { type: Function },
};

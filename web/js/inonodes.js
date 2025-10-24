import { app } from "../../../scripts/app.js";
import { applyTextReplacements } from "../../../scripts/utils.js";

app.registerExtension({
	name: "InoNodes.jsnodes",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if(!nodeData?.category?.startsWith("InoNodes")) {
			return;
		  }
		switch (nodeData.name) {
			case "InoConditionBooleanMulti":
				const originalOnNodeCreated = nodeType.prototype.onNodeCreated || function() {};
				nodeType.prototype.onNodeCreated = function () {
					originalOnNodeCreated.apply(this, arguments);

					this._type = "BOOLEAN";
					this.addWidget("button", "Update inputs", null, () => {
						if (!this.inputs) {
							this.inputs = [];
						}
						const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
						const num_inputs = this.inputs.filter(input => input.name && input.name.toLowerCase().includes("bool_")).length
						if (target_number_of_inputs === num_inputs) return; // already set, do nothing

						if(target_number_of_inputs < num_inputs){
							const inputs_to_remove = num_inputs - target_number_of_inputs;
							for(let i = 0; i < inputs_to_remove; i++) {
								this.removeInput(this.inputs.length - 1);
							}
						}
						else{
							for(let i = num_inputs+1; i <= target_number_of_inputs; ++i)
								this.addInput(`bool_${i}`, this._type, {shape: 7});
						}
					});
				}
				break;
		}

	},
	async setup() {
	}
});

package {{ package }};

import java.util.List;
import java.util.stream.Stream;

import org.optaplanner.core.api.domain.entity.PlanningEntity;
import org.optaplanner.core.api.domain.variable.CustomShadowVariable;
import org.optaplanner.core.api.domain.variable.PlanningVariableReference;

import com.ibm.hrl.scenoptic.keys.AbstractCellKey;
import com.ibm.hrl.scenoptic.algorithms.CellListener;
import com.ibm.hrl.scenoptic.domain.descriptors.Formula;
import com.ibm.hrl.scenoptic.domain.{{ shadow_cell_class }};

@PlanningEntity
public class {{ scenario_name }}{{ shadow_cell_class }}<T> extends {{ shadow_cell_class }}<AbstractCellKey, T> {
	public {{ scenario_name }}{{ shadow_cell_class }}() {
	}

	public {{ scenario_name }}{{ shadow_cell_class }}(AbstractCellKey key, List<AbstractCellKey> predecessors, Formula formula) {
		super(key, predecessors, formula);
	}

	@Override
	@CustomShadowVariable(variableListenerClass = CellListener.class, sources = {
{% for name in planning_classes | sort %}
			@PlanningVariableReference(entityClass = {{ scenario_name }}{{ name }}.class, variableName = "value"){{ ',\n' if not loop.last }}
{%- endfor %} })
	public T getValue() {
		return super.getValue();
	}

	@Override
	public void setValue(T value) {
		super.setValue(value);
	}
}

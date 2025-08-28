package {{ package }};

import org.optaplanner.core.api.domain.entity.PlanningEntity;
import org.optaplanner.core.api.domain.variable.PlanningVariable;

import com.ibm.hrl.scenoptic.domain.PlanningCell;

@PlanningEntity
public class {{ scenario_name }}{{ planning_class }}<K extends Comparable<K>> extends PlanningCell<K, {{ java_type }}> {
	public {{ scenario_name }}{{ planning_class }}() {
	}

	public {{ scenario_name }}{{ planning_class }}(K key) {
		super(key);
	}

	@Override
	@PlanningVariable(valueRangeProviderRefs = "{{ planning_class }}")
	public {{ java_type }} getValue() {
		return super.getValue();
	}

	@Override
	public void setValue({{ java_type }} value) {
		super.setValue(value);
	}
}

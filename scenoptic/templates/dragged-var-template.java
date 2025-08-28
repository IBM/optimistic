package {{ package }};

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

import com.google.common.collect.Streams;

import org.optaplanner.core.api.domain.entity.PlanningEntity;
import org.optaplanner.core.api.domain.variable.CustomShadowVariable;
import org.optaplanner.core.api.domain.variable.PlanningVariableReference;

import com.ibm.hrl.scenoptic.keys.AbstractCellKey;
import com.ibm.hrl.scenoptic.domain.CellListener;
import com.ibm.hrl.scenoptic.domain.PredecessorFormula;
import com.ibm.hrl.scenoptic.domain.Formula;
import com.ibm.hrl.scenoptic.domain.DraggedCell;

@PlanningEntity
public class {{ scenario_name }}DraggedCell<T> extends DraggedCell<AbstractCellKey, T> {
	public {{ scenario_name }}DraggedCell() {
	}

	public {{ scenario_name }}DraggedCell(AbstractCellKey key, List<AbstractCellKey> predecessors, Formula formula, PredecessorFormula<AbstractCellKey> predecessorFormula) {
		super(key, predecessors, formula, predecessorFormula);
	}

    @Override
    public Stream<AbstractCellKey> getPredecessors() {
        return Streams.concat(Arrays.stream(predecessorFormula.apply(key)),
                predecessors.stream().flatMap(AbstractCellKey::getElements));
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

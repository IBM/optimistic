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
import com.ibm.hrl.scenoptic.domain.IncrementalPredecessorFormula;
import com.ibm.hrl.scenoptic.domain.IncrementalUpdateFormula;
import com.ibm.hrl.scenoptic.domain.IncrementalFreshFormula;
import com.ibm.hrl.scenoptic.domain.InitializationTriggerCell;
import com.ibm.hrl.scenoptic.domain.IncrementalInitializer;
import com.ibm.hrl.scenoptic.domain.DraggedIncrementalCell;
import com.ibm.hrl.scenoptic.domain.PredecessorFormula;

@PlanningEntity
public class {{ scenario_name }}DraggedIncrementalCell<T> extends DraggedIncrementalCell<AbstractCellKey, T> {
	public {{ scenario_name }}DraggedIncrementalCell() {
	}

	public {{ scenario_name }}DraggedIncrementalCell(AbstractCellKey key, List<AbstractCellKey> predecessors, int numberOfPredecessorLists, IncrementalPredecessorFormula<AbstractCellKey> incrementalPredecessors,
                           IncrementalUpdateFormula incrementalUpdateFormula, IncrementalFreshFormula incrementalFreshFormula,
                           PredecessorFormula<AbstractCellKey> predecessorFormula, IncrementalInitializer<T> initializer) {
		super(key, predecessors, numberOfPredecessorLists, incrementalPredecessors, incrementalUpdateFormula, incrementalFreshFormula, predecessorFormula, initializer);
	}

    @Override
    public Stream<AbstractCellKey> getPredecessors() {
        return Streams.concat(Arrays.stream(predecessorFormula.apply(key)),
                predecessors.stream().flatMap(AbstractCellKey::getElements));
    }

	@Override
	@CustomShadowVariable(variableListenerClass = CellListener.class, sources = {
{% for name in planning_classes | sort %}
			@PlanningVariableReference(entityClass = {{ scenario_name }}{{ name }}.class, variableName = "value"),
{% endfor %}
			@PlanningVariableReference(entityClass = InitializationTriggerCell.class, variableName = "value") })
	public T getValue() {
		return super.getValue();
	}

	@Override
	public void setValue(T value) {
		super.setValue(value);
	}
}

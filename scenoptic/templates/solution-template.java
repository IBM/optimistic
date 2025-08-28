package {{ package }};

import java.util.List;

import org.optaplanner.core.api.domain.solution.PlanningScore;
import org.optaplanner.core.api.domain.solution.PlanningSolution;
import org.optaplanner.core.api.domain.valuerange.ValueRange;
import org.optaplanner.core.api.domain.valuerange.ValueRangeFactory;
import org.optaplanner.core.api.domain.valuerange.ValueRangeProvider;
import org.optaplanner.core.api.score.Score;
import org.optaplanner.core.api.score.buildin.bendable.BendableScore;

import com.ibm.hrl.scenoptic.domain.IncrementalCell;
import com.ibm.hrl.scenoptic.domain.InputCell;
import com.ibm.hrl.scenoptic.domain.PlanningCell;
import com.ibm.hrl.scenoptic.domain.ShadowCell;
import com.ibm.hrl.scenoptic.domain.SpreadsheetProblem;
import com.ibm.hrl.scenoptic.domain.ISummingCell;

@PlanningSolution
public class {{ scenario_name }}Solution<K extends Comparable<K>> extends SpreadsheetProblem<K> {
	@PlanningScore(bendableHardLevelsSize = {{ n_hard }}, bendableSoftLevelsSize = {{ n_soft }})
	private BendableScore score;

	// No-arg constructor required for OptaPlanner
	public {{ scenario_name }}Solution() {
	}

	public {{ scenario_name }}Solution(List<? extends PlanningCell<K, Integer>> decisions,
	        List<? extends ShadowCell<K, ?>> cells,
			List<? extends InputCell<K, ?>> inputs,
			List<? extends IncrementalCell<K, ?>> incrementals,
			List<? extends ISummingCell<K, ?>> summingCells) {
		super(decisions, cells, inputs, incrementals, summingCells);
	}

{% for cls in planning_classes | sort(attribute="name") %}
	@ValueRangeProvider(id = "{{ cls.name }}")
{% if 'constructor' in cls %}
	public ValueRange<{{ cls.type }}> get{{ cls.name }}Range() {
		return {{ cls.constructor }};
	}
{% else %}
	private List<{{ cls.type }}> range{{ cls.name }} = {{ cls.value }};
{% endif %}

{% endfor %}
    @Override
	public BendableScore getScore() {
		return score;
	}

    @Override
	public void setScore(Score score) {
		this.score = (BendableScore) score;
	}
}

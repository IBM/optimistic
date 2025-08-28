package {{ package}};

import static com.ibm.hrl.scenoptic.utils.ScenopticUtils.*;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

import net.sourceforge.argparse4j.inf.ArgumentParserException;

import org.optaplanner.core.api.score.buildin.bendable.BendableScore;
import org.optaplanner.core.api.score.calculator.EasyScoreCalculator;

import com.ibm.hrl.scenoptic.keys.CellKey;
import com.ibm.hrl.scenoptic.keys.AdHocRangeKey;
import com.ibm.hrl.scenoptic.keys.PredecessorCellKey;
import com.ibm.hrl.scenoptic.keys.RangeDistance;
import com.ibm.hrl.scenoptic.keys.CellDistance;
import com.ibm.hrl.scenoptic.keys.FixedDistance;
import com.ibm.hrl.scenoptic.domain.Cell;
import com.ibm.hrl.scenoptic.domain.descriptors.Formula;
import com.ibm.hrl.scenoptic.domain.IncrementalCell;
import com.ibm.hrl.scenoptic.domain.descriptors.IncrementalPredecessorFormula;
import com.ibm.hrl.scenoptic.domain.descriptors.IncrementalUpdateFormula;
import com.ibm.hrl.scenoptic.domain.descriptors.IncrementalFreshFormula;
import com.ibm.hrl.scenoptic.domain.InputCell;
import com.ibm.hrl.scenoptic.domain.PlanningCell;
import com.ibm.hrl.scenoptic.domain.ShadowCell;
import com.ibm.hrl.scenoptic.domain.SpreadsheetProblem;
import com.ibm.hrl.scenoptic.domain.initialization.IncrementalInitializer;
import com.ibm.hrl.scenoptic.domain.initialization.IntegerInitializer;
import com.ibm.hrl.scenoptic.domain.initialization.DoubleInitializer;
import com.ibm.hrl.scenoptic.info.DecisionCellInfo;
import com.ibm.hrl.scenoptic.info.ShadowCellInfo;
import com.ibm.hrl.scenoptic.info.IncrementalCellInfo;
import com.ibm.hrl.scenoptic.keys.AbstractCellKey;
import com.ibm.hrl.scenoptic.keys.AdHocRangeKey;
import com.ibm.hrl.scenoptic.keys.CellKey;
import com.ibm.hrl.scenoptic.main.SpreadsheetOptimizationMain;
import com.ibm.hrl.scenoptic.info.SummingCellInfo;
import com.ibm.hrl.scenoptic.domain.ISummingCell;
{% if summing[0] %}
import com.ibm.hrl.scenoptic.domain.CountingShadowCellImpl;
import com.ibm.hrl.scenoptic.domain.SummingShadowCellImpl;
import com.ibm.hrl.scenoptic.domain.ConstructingFormula;
import com.ibm.hrl.scenoptic.domain.processors.SingleIntSummingCreator;
{% endif %}

{% if domain_package != package %}
{% for class_suffix in entity_classes %}
import {{ domain_package }}.{{ scenario_name }}{{ class_suffix }};
{% endfor %}
import {{ domain_package }}.{{ scenario_name }}ShadowCell;
import {{ domain_package }}.{{ scenario_name }}IncrementalCell;
{% if summing[0] %}
import {{ domain_package }}.{{ scenario_name }}CountingShadowCell;
{% endif %}
{% endif %}
{% if solver_package != package %}
import {{ solver_package }}.{{ scenario_name }}Solution;
import {{ solver_package }}.{{ scenario_name }}ScoreCalculator;
{% endif %}

public class {{ scenario_name }}Main extends SpreadsheetOptimizationMain<AbstractCellKey> {
	private static final List<PredecessorCellKey> PREDECESSORS_KEYS = List.of(
{% for e in predecessors[0] | sort(attribute="key")%}
            new PredecessorCellKey(new CellKey({{ normalize_java_vars(e.cell.sheet) }}, {{ e.cell.row }}, {{ e.cell.col }}),
					List.of(
{%- for cell in e.fixed_cells %}
new FixedDistance({{ normalize_java_vars(cell[0]) }}, {{ cell[1] }}, {{ cell[2] }}){{ ',\n                            ' if not loop.last }}
{%- endfor %}
{% if e.fixed_cells | length > 0  and (e.cells_category | length > 0 or e.range_category | length > 0) %}{{ ',\n                            '  }}{% endif %}
{%- for cell in e.cells_category %}
new CellDistance({{ normalize_java_vars(cell[0]) }}, {{ cell[1] }}, {{ cell[2] }}){{ ',\n                            ' if not loop.last }}
{%- endfor %}
{% if e.cells_category | length > 0  and e.range_category | length > 0 %}{{ ',\n                            '  }}{% endif %}
{%- for arange in e.range_category %}
new RangeDistance({{ normalize_java_vars(arange[0]) }}, {{ arange[1] }}, {{ arange[2] }}, {{ arange[3] }}, {{ arange[4] }}){{ ', ' if not loop.last }}
{%- endfor %})){{ ',\n' if not loop.last }}
{%- endfor %}
{% if predecessors[1] | length > 0  and predecessors[0] | length > 0 %}
,
{% endif %}
{% for e in predecessors[1] | sort(attribute="key") %}
            new PredecessorCellKey(new AdHocRangeKey({{ normalize_java_vars(e.range.sheet) }}, {{ e.range.start_row }}, {{ e.range.end_row }}, {{ e.range.start_col }}, {{ e.range.end_col }}),
					List.of(
{%- for cell in e.fixed_cells %}
new FixedDistance({{ normalize_java_vars(cell[0]) }}, {{ cell[1] }}, {{ cell[2] }}){{ ',\n                            ' if not loop.last }}
{%- endfor %}
{% if e.fixed_cells | length > 0  and (e.cells_category | length > 0 or e.range_category | length > 0) %}{{ ',\n                            '  }}{% endif %}
{%- for cell in e.cells_category %}
new CellDistance({{ normalize_java_vars(cell[0]) }}, {{ cell[1] }}, {{ cell[2] }}){{ ',\n                            ' if not loop.last }}
{%- endfor %}
{% if e.cells_category | length > 0  and e.range_category | length > 0 %}{{ ',\n                            ' if not loop.last }}{% endif %}
{%- for arange in e.range_category %}
new RangeDistance({{ normalize_java_vars(arange[0]) }}, {{ arange[1] }}, {{ arange[2] }}, {{ arange[3] }}, {{ arange[4] }}){{ ',\n                            ' if not loop.last }}
{%- endfor %})){{ ',\n' if not loop.last }}
{%- endfor %}
);


{% for func in functions %}
    private {{ func.type }} {{ func.name }} = {{ func.code }};
{% endfor %}

	public Stream<AbstractCellKey> getInputInfo() {
	    return Stream.of(
{% for e in inputs[0] | sort(attribute="key")%}
            new CellKey({{ normalize_java_vars(e.cell.sheet) }}, {{ e.cell.row }}, {{ e.cell.col }}){{ ',\n' if not loop.last }}
{%- endfor %}
{% if inputs[1] | length > 0  and inputs[0] | length > 0 %}
,
{% endif %}
{% for e in inputs[1] | sort(attribute="key")%}
            new AdHocRangeKey({{ normalize_java_vars(e.range.sheet) }}, {{ e.range.start_row }}, {{ e.range.end_row }}, {{ e.range.start_col }}, {{ e.range.end_col }}){{ ',\n' if not loop.last }}
{%- endfor %});
    }

	public List<DecisionCellInfo<AbstractCellKey>> getDecisionInfo() {
		return List.of(
{% for e in decisions[0] | sort(attribute="key")%}
			new DecisionCellInfo<>(new CellKey({{ normalize_java_vars(e.cell.sheet) }}, {{ e.cell.row }}, {{ e.cell.col }}), {{ scenario_name }}{{ e.class_suffix }}::new){{ ',\n' if not loop.last }}
{%- endfor %}
{% if decisions[1] | length > 0  and decisions[0] | length > 0 %}
,
{% endif %}
{% for e in decisions[1] | sort(attribute="key")%}
            new DecisionCellInfo<>(new AdHocRangeKey({{ normalize_java_vars(e.range.sheet) }}, {{ e.range.start_row }}, {{ e.range.end_row }}, {{ e.range.start_col }}, {{ e.range.end_col }}), {{ scenario_name }}{{ e.class_suffix }}::new){{ ',\n' if not loop.last }}
{%- endfor %});
    }

	public List<ShadowCellInfo<AbstractCellKey>> getShadowCellInfo() {
		return List.of(
{% for e in dvars[0] | sort(attribute="key")%}
            new ShadowCellInfo<>(new CellKey({{ normalize_java_vars(e.cell.sheet) }}, {{ e.cell.row }}, {{ e.cell.col }}), {{ e.formula }}){{ ',\n' if not loop.last }}
{%- endfor %}
{% if dvars[1] | length > 0  and dvars[0] | length > 0 %}
,
{% endif %}
{% for e in dvars[1] | sort(attribute="key")%}
            new ShadowCellInfo<>(new AdHocRangeKey({{ normalize_java_vars(e.range.sheet) }}, {{ e.range.start_row }}, {{ e.range.end_row }}, {{ e.range.start_col }}, {{ e.range.end_col }}), {{ e.formula }}){{ ',\n' if not loop.last }}
{%- endfor %});
    }

    public List<SummingCellInfo<AbstractCellKey>> getSummingCellInfo() {
		return List.of(
{% for e in summing[0] | sort(attribute="key")%}
            new SummingCellInfo<>(new CellKey({{ normalize_java_vars(e.cell.sheet) }}, {{ e.cell.row }}, {{ e.cell.col }}), {{ e.creator }}){{ ',\n' if not loop.last }}
{%- endfor %}
{% if summing[1] | length > 0  and summing[0] | length > 0 %}
,
{% endif %}
{% for e in summing[1] | sort(attribute="key")%}
            new SummingCellInfo<>(new AdHocRangeKey({{ normalize_java_vars(e.range.sheet) }}, {{ e.range.start_row }}, {{ e.range.end_row }}, {{ e.range.start_col }}, {{ e.range.end_col }}), {{ e.formula }}){{ ',\n' if not loop.last }}
{%- endfor %});
    }

	@Override
	public Set<AbstractCellKey> getNonStrictCells() {
{% if not non_strict_cells %}
        return Collections.emptySet();
{% else %}
		return Stream.of({% for cell in non_strict_cells | sort %}{{ normalize_java_vars(cell.name) }}{{ ',' if not loop.last }} {% endfor %}).collect(Collectors.toSet());
{% endif %}
	}

	public Map<AbstractCellKey, AbstractCellKey[]> getPredecessorInfo() {
		return predecessors;
    }

	public List<IncrementalCellInfo<AbstractCellKey>> getIncrementalInfo() {
		return List.of(
{% for e in incremental[0] | sort(attribute="key")%}
			new IncrementalCellInfo<>(new CellKey({{ normalize_java_vars(e.cell.sheet) }}, {{ e.cell.row }}, {{ e.cell.col }}), {{ e.n_preds }}, {{ e.formula }}, {{ e.update_formula }}, {{ e.fresh_formula }}, {{ e.element_type }}){{ ',\n' if not loop.last }}
{%- endfor %}
{% if incremental[1] | length > 0  and incremental[0] | length > 0 %}
,
{% endif %}
{% for e in incremental[1] | sort(attribute="key")%}
            new IncrementalCellInfo<>(new AdHocRangeKey({{ normalize_java_vars(e.range.sheet) }}, {{ e.range.start_row }}, {{ e.range.end_row }}, {{ e.range.start_col }}, {{ e.range.end_col }}), {{ e.n_preds }}, {{ e.formula }}, {{ e.update_formula }}, {{ e.fresh_formula }}, {{ e.element_type }}){{ ',\n' if not loop.last }}
{%- endfor %});
	}

	@Override
	public ShadowCell<AbstractCellKey, ?> createShadowVariable(AbstractCellKey key, List<AbstractCellKey> predecessors, Formula formula) {
		return new {{ scenario_name }}ShadowCell<>(key, predecessors, formula);
	}

	@Override
	public IncrementalCell<AbstractCellKey, ?> createIncrementalVariable(
            AbstractCellKey key, List<AbstractCellKey> predecessors, int numberOfPredecessorLists,
            IncrementalPredecessorFormula<AbstractCellKey> incrementalPredecessors, IncrementalUpdateFormula incrementalUpdateFormula,
            IncrementalFreshFormula incrementalFreshFormula, IncrementalInitializer<?> initializer) {
		return new {{ scenario_name }}IncrementalCell<>(key, predecessors, numberOfPredecessorLists, incrementalPredecessors, incrementalUpdateFormula, incrementalFreshFormula, initializer);
	}

	@Override
	public SpreadsheetProblem<AbstractCellKey> createSolution(
	        List<? extends PlanningCell<AbstractCellKey, ?>> decisions,
			List<? extends ShadowCell<AbstractCellKey, ?>> cells,
			List<? extends InputCell<AbstractCellKey, ?>> inputs,
			List<? extends IncrementalCell<AbstractCellKey, ?>> incrementals,
			List<? extends ISummingCell<AbstractCellKey, ?>> summingCells) {
		return new {{ scenario_name }}Solution(decisions, cells, inputs, incrementals, summingCells);
	}

	@Override
	public Class<? extends SpreadsheetProblem<AbstractCellKey>> getSolutionClass() {
		return (Class<? extends SpreadsheetProblem<AbstractCellKey>>) {{ scenario_name }}Solution.class;
	}

	@Override
	public Class<Cell<AbstractCellKey, ?>>[] getEntityClasses() {
		return new Class[] { {% for cls in entity_classes %}{{ scenario_name }}{{ cls }}.class, {% endfor %} {{ scenario_name }}ShadowCell.class, {{ scenario_name }}IncrementalCell.class
{%- if summing[0] %}
, {{ scenario_name }}CountingShadowCell.class
{%- endif %}
 };
	}

	public Class<? extends EasyScoreCalculator<? extends SpreadsheetProblem<AbstractCellKey>, BendableScore>> getScoreCalculatorClass() {
		return {{ scenario_name }}ScoreCalculator.class;
	}

	public static void main(String[] args) throws ArgumentParserException {
		new {{ scenario_name }}Main().mainBody(args, PREDECESSORS_KEYS);
	}
}

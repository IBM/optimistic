package {{ package }};

import org.optaplanner.core.api.score.buildin.bendable.BendableScore;
import org.optaplanner.core.api.score.calculator.EasyScoreCalculator;

import com.ibm.hrl.scenoptic.keys.AbstractCellKey;
import com.ibm.hrl.scenoptic.keys.CellKey;
import com.ibm.hrl.scenoptic.solver.SpreadsheetScoreCalculator;

public class {{ scenario_name }}ScoreCalculator extends SpreadsheetScoreCalculator<AbstractCellKey, {{ scenario_name }}Solution<AbstractCellKey>>
implements EasyScoreCalculator<{{ scenario_name }}Solution<AbstractCellKey>, BendableScore> {
   	protected BendableScore zero = BendableScore.zero({{ hard_exprs | length }}, {{ soft_exprs | length }});

	@Override
	public BendableScore calculateScore({{ scenario_name }}Solution<AbstractCellKey> solution) {
		try {
			return BendableScore.of(
					new int[] { {% for expr in hard_exprs %}{{ expr }}{{ ',\n\t\t\t\t\t           ' if not loop.last }} {% endfor %}},
					new int[] { {% for expr in soft_exprs %}{{ expr }}{{ ',\n\t\t\t\t\t           ' if not loop.last }} {% endfor %}});
		} catch (MissingValue e) {
			return zero;
		}
	}
}

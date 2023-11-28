function predictOutcome() {
    var battingTeam = document.getElementById('battingTeam').value;
    var bowlingTeam = document.getElementById('bowlingTeam').value;
    var venue = document.getElementById('venue').value;
    var target = parseInt(document.getElementById('target').value);
    var score = parseInt(document.getElementById('score').value);
    var overs = parseInt(document.getElementById('overs').value);
    var wickets = parseInt(document.getElementById('wickets').value);

    var modalOutput = document.getElementById('modalOutput');

    // Input validation
    if (!(0 <= target && target <= 300 && 0 <= overs && overs <= 20 && 0 <= wickets && wickets <= 10 && 0 <= score)) {
        modalOutput.textContent = 'There is something wrong with the input, please fill in the correct details as of IPL T-20 format';
        return;
    }

    try {
        var runsLeft = target - score;
        var ballsLeft = 120 - overs * 6;
        var wicketsLeft = 10 - wickets;
        var currentRunRate = score / overs;
        var requiredRunRate = (runsLeft * 6) / ballsLeft;

        // Placeholder for prediction logic - replace with your own algorithm
        var winProbability = calculateWinProbability(currentRunRate, requiredRunRate, wicketsLeft);

        modalOutput.innerHTML = `
            <p>${battingTeam} - ${Math.round(winProbability * 100)}%</p>
            <p>${bowlingTeam} - ${Math.round((1 - winProbability) * 100)}%</p>
        `;

    } catch (error) {
        modalOutput.textContent = 'Please fill in all the required details';
    }

    var modal = document.getElementById('myModal');
    modal.style.display = 'block';
}

// Function to calculate win probability (replace with your own algorithm)
function calculateWinProbability(currentRunRate, requiredRunRate, wicketsLeft) {
    // Placeholder logic - replace with your own calculation
    // For simplicity, let's say higher run rate, more wickets, and fewer runs remaining increase win probability
    var baseProbability = 0.5;
    var runRateFactor = currentRunRate / requiredRunRate;
    var wicketsFactor = wicketsLeft / 10;

    return baseProbability + 0.2 * runRateFactor - 0.1 * wicketsFactor;
}

function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

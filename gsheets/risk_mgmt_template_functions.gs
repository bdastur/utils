/** @OnlyCurrentDoc */

function parseRiskTable() {
    var spreadsheet = SpreadsheetApp.getActive();
    var tableRows = [8,9,10,11,12,13,14,15];
    var tableImpactColumn = 'D';
    var tableProbabilityColumn = 'E';
    
    for( var row in tableRows) {
      console.log(tableRows[row]);
      var impactString = tableImpactColumn + tableRows[row];
      var impact = spreadsheet.getRange(impactString).getValue()
      if (impact) {
        console.log("Impact: " + impact);
      }

      var probabilityString = tableProbabilityColumn + tableRows[row];
      var probability = spreadsheet.getRange(probabilityString).getValue();
      if (probability) {
        console.log("Probability: " + probability);
      }
    }

}
 
/*
 * resetRiskMatrix
 * Clears the contents for all the cells of the risk matrix.
 * Parameters:
 *   matrixColumns: A list of Columns
 *   matrixRows:    A list of row numbers
 * Returns:
 *   None
 */
function resetRiskMatrix(matrixColumns, matrixRows) {
    var spreadsheet = SpreadsheetApp.getActive();
    for (row in matrixRows) {
      for (col in matrixColumns) {
        var cellString = matrixColumns[col] + matrixRows[row];
        console.log("CellString: " + cellString);
        spreadsheet.getRange(cellString).clearContent();
      }
    }
}

/*
 * populateRiskMatrix
 * Populates the 5x5 matrix with the risk numbers based on
 * each risk's impact and probability.
 * Parameters:
 *   None
 * Returns:
 *   None
 */
function populateRiskMatrix() {
  var spreadsheet = SpreadsheetApp.getActive();
  var matrixColumns = ['I', 'J', 'K', 'L', 'M'];
  var matrixRows = [12, 11, 10, 9, 8, 7];

  resetRiskMatrix(matrixColumns, matrixRows);
  
  // Risk table.
  var tableRows = [8,9,10,11,12,13,14,15];
  var tableImpactColumn = 'D';
  var tableProbabilityColumn = 'E';
  var tableRiskNoColumn = 'B';

  for( var row in tableRows) {
    console.log(tableRows[row]);
    var impactString = tableImpactColumn + tableRows[row];
    var probabilityString = tableProbabilityColumn + tableRows[row];
    var riskNoString = tableRiskNoColumn + tableRows[row];

    var riskNo = spreadsheet.getRange(riskNoString).getValue();
    var impact = spreadsheet.getRange(impactString).getValue()
    var probability = spreadsheet.getRange(probabilityString).getValue();
    if (! impact || ! probability) {
      console.log("impact or probability not set. continue.");
      continue;
    }
    var cellString = matrixColumns[probability-1] + matrixRows[impact-1];
    var cellValue = spreadsheet.getRange(cellString).getValue();
    cellValue = cellValue + "," + riskNo;
    spreadsheet.getRange(cellString).setValue(cellValue);
  }

}





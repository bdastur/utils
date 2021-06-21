function testmacro() {
  var spreadsheet = SpreadsheetApp.getActive();
  console.log("Spreadhseet: " + spreadsheet);
  console.log("Spreadsheet id: " + spreadsheet.getId());
  spreadsheet.getRange('D1').activate();
  console.log("Test");
  Logger.log(SpreadsheetApp.getActive().getUrl());
  spreadsheet.getCurrentCell().setValue('Project name');
  spreadsheet.getRange('D2').activate();
  spreadsheet.getCurrentCell().setValue('ILM automation');
  spreadsheet.getRange('D1').activate();
  spreadsheet.getActiveRangeList().setFontWeight('bold');
  spreadsheet.getRange('D3').activate();
};

function onEdit(e){
  // Set a comment on the edited cell to indicate when it was changed.
  var range = e.range;
  console.log("Type of e: " + typeof(e));
  range.setValue(new Date());
  //e.setValue = new Date();
  console.log("Current cell: " + e.getRange());
  range.setNote('Last modified: ' + new Date());
}
function getAllRanges() {
  var spreadsheet = SpreadsheetApp.getActive();
  //Get spreadsheet name
  sheetName = spreadsheet.getSheetName();
  console.log("Sheet name: " + sheetName);

  //get spreadsheet values. (row start, col start, no of rows, no of cols)
  values = spreadsheet.getSheetValues(1, 1, 1, 5);
  console.log("Values: " + values);

}

function macro2() {
  console.log("Macro2");
  var spreadsheet = SpreadsheetApp.getActive();
  spreadsheet.getRange('G11:I11').activate();
  spreadsheet.getActiveRangeList().setBackground('#00ff00');

};

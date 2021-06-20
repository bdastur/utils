function testmacro() {
  var spreadsheet = SpreadsheetApp.getActive();
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
  range.setNote('Last modified: ' + new Date());
}

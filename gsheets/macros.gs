function testmacro() {
  var spreadsheet = SpreadsheetApp.getActive();
  console.log("Spreadhseet: " + spreadsheet.getBlob());
  console.log("Spreadhseet json: " + JSON.stringify(spreadsheet));
  
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

// function onEdit(e){
//   // Set a comment on the edited cell to indicate when it was changed.
//   var range = e.range;
//   console.log("Type of e: " + typeof(e));
//   range.setValue(new Date());
//   //e.setValue = new Date();
//   console.log("Current cell: " + e.getRange());
//   range.setNote('Last modified: ' + new Date());
// }
function getAllRanges() {
  var spreadsheet = SpreadsheetApp.getActive();
  //Get spreadsheet name
  var sheetName = spreadsheet.getSheetName();
  console.log("Sheet name: " + sheetName);

  //get spreadsheet values. (row start, col start, no of rows, no of cols)
  var headers = spreadsheet.getSheetValues(1, 1, 1, 5);
  console.log("Values: " + values);
  //Get data range
  var range = spreadsheet.getDataRange();
  var values = range.getValues();
  for (var i = 0; i < values.length; i++) {
    var row = "";
    for (var j = 0; j < values[i].length; j++) {
      if (values[i][j]) {
        row = row + values[i][j]
      }
      row = row + ",";
    }
    Logger.log(row); 
  }

  // Get range for specific sheet.
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet()
  var optionSheet = spreadsheet.getSheetByName("options");
  console.log("Option sheet name: " + optionSheet.getSheetName());
  var range = optionSheet.getDataRange();
  var values = range.getValues();

  var rowString = ""
  for (var row in values) {
    rowString = "Row: "
    for (var column in values[row]) {
      if (values[row][column]) {
        rowString = rowString + values[row][column]
      }
      rowString = rowString + ",";
    }
    Logger.log(rowString); 
  }



}

function macro2() {
  console.log("Macro2");
  var spreadsheet = SpreadsheetApp.getActive();
  spreadsheet.getRange('G11:I11').activate();
  spreadsheet.getActiveRangeList().setBackground('#00ff00');

};

function datavalidationmacro_1() {
  var spreadsheet = SpreadsheetApp.getActive();
  spreadsheet.getRange('A1:A6').activate();
  spreadsheet.getRange('A1:A6').setDataValidation(SpreadsheetApp.newDataValidation()
  .setAllowInvalid(true)
  .requireValueInRange(spreadsheet.getRange('\'Dropdown Menu\'!$A$1:$A$6'), true)
  .build());
  spreadsheet.setActiveSheet(spreadsheet.getSheetByName('Sheet1'), true);
};

function readEntryForm() {
  var entrySheetName = "entryform"
  // Get range for specific sheet.
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet()
  var entrySheet = spreadsheet.getSheetByName(entrySheetName);
  console.log("Option sheet name: " + entrySheet.getSheetName());
  var taskName = entrySheet.getRange(3,3).getValue();
  var taskDescription = entrySheet.getRange(4,3).getValue()
  var taskCategory = entrySheet.getRange(5,3).getValue()
  var taskEstimatedDuration = entrySheet.getRange(6,3).getValue()
  var taskStartDate = entrySheet.getRange(7,3).getValue()
  var taskPriority = entrySheet.getRange(8,3).getValue()
  var taskOwner = entrySheet.getRange(9,3).getValue()

  var entryString = "Taskname: " + taskName + ", Description: " + taskDescription + ", Category: " + taskCategory 
      + ", duration: " + taskEstimatedDuration
  console.log("Data entries: " + entryString);
  populatePlanningSheet(taskName);
}

function populatePlanningSheet(taskName) {
  console.log("Populate main planning sheet " + taskName);
  var sheetName = "main-planning-sheet"
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet()
  var mainSheet = spreadsheet.getSheetByName(sheetName);
  console.log("Option sheet name: " + mainSheet.getSheetName());
  var range = mainSheet.getDataRange();
  var values = range.getValues();

  var rowString = ""
  var rowId = 1;
  var startRowId = 6;
  var columnId = 1
  var tasklist = [];
  for (var row in values) {
    var taskObj = {};
    if (rowId < startRowId) {
      rowId = rowId + 1;
      continue;
    }
    rowString = "Row: " + rowId + " : ";
    var columnId = 1;
    taskObj['description'] = values[row][2];
    taskObj['category'] = values[row][3];
    taskObj['owner'] = values[row][4];
    console.log("HERE: " + values[row][2]);

    // for (var column in values[row]) {
    //   var cellValue = values[row][column]
    //   if (cellValue) {
    //     rowString = rowString + "COl: " + columnId + " : "+ values[row][column]
    //   } 
      
    //   rowString = rowString + ",";
    //   columnId = columnId + 1;
    // }
    tasklist.push(taskObj)
    Logger.log(rowString); 
    rowId = rowId + 1;
  }

  console.log("Task list: " + JSON.stringify(tasklist));

}



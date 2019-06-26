function searchRows(tblId) {
var tbl = document.getElementById(tblId);
var headRow = tbl.rows[0];
var arrayOfHTxt = new Array();
var arrayOfHtxtCellIndex = new Array();

for (var v = 0; v < headRow.cells.length; v++) {
    if (headRow.cells[v].getElementsByTagName('input')[0]) {
        var Htxtbox = headRow.cells[v].getElementsByTagName('input')[0];
            if (Htxtbox.value.replace(/^\s+|\s+$/g, '') != '') {
            arrayOfHTxt.push(Htxtbox.value.replace(/^\s+|\s+$/g, ''));
            arrayOfHtxtCellIndex.push(v);
        }
    }
}

for (var i = 1; i < tbl.rows.length; i++) {
    tbl.rows[i].style.display = 'table-row';
    for (var v = 0; v < arrayOfHTxt.length; v++) {
        var CurCell = tbl.rows[i].cells[arrayOfHtxtCellIndex[v]];
        var CurCont = CurCell.innerHTML.replace(/<[^>]+>/g, "");
        var reg = new RegExp(arrayOfHTxt[v] + ".*", "i");
        if (CurCont.match(reg) == null) {
            tbl.rows[i].style.display = 'none';
        }
    }
}
}
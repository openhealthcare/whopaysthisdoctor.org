let search = {
  rows: [],
  matches: []
}
  
search.init = function(searchElement, tableElement) {
  this.searchElement = searchElement;
  this.tableElement = tableElement;
  this.noResultsElement = document.getElementById('no-results');
  this.processRows();
  this.addEvents();
}

search.processRows = function() {
  let rowElements = this.tableElement.querySelectorAll('tr.doctor');
  for(let i = 0; i < rowElements.length; i++) {
    let row = rowElements[i];
    let fields = row.querySelectorAll('td');
    let name = fields[0].innerText;
    let position = fields[3].innerText;
    this.rows.push({
      text: name + position,
      element: row
    });
  }
}
  
search.addEvents = function() {
  this.searchElement.addEventListener('keyup', (event) => {
    this.doSearch(event.target.value);
  });
  this.searchElement.addEventListener('change', (event) => {
    this.doSearch(event.target.value);
  });
}
  
search.searchRows = function(string) {
  string = string.trim().toLowerCase();
  let matches = [];
  for(let i = 0; i < this.rows.length; i++) {
    let target = this.rows[i].text.trim().toLowerCase();
    if ( target.indexOf(string) == -1 ) {
      this.rows[i].element.style.display = "none";
    } else {
      this.rows[i].element.style.display = "table-row";
      matches.push(i);
    };
  }
  if( matches.length == 0 ) {
    this.noResultsElement.style.display = "table-row";
  } else {
    this.noResultsElement.style.display = "none";
  }
}
  
search.doSearch = function(keyword) {
  if ( this.searchTimeoutID ) {
    window.clearTimeout(this.searchTimeoutID);
  }
  this.searchElement.classList.add('loading');
  this.searchTimeoutID = window.setTimeout(()=>{
    this.searchRows(keyword);
    this.searchTimeoutID = null;
  }, 200);
}

let table = document.getElementById('doctor-table');
if( table ) {
  search.init(
    document.getElementById('search-field'),
    table,
  );
}

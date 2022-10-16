var day_button = document.getElementById("day_button")
var week_button = document.getElementById("week_button")
var month_button = document.getElementById("month_button")
var year_button = document.getElementById("year_button")

var tbodyRef = document.getElementById("main_table").getElementsByTagName("tbody")[0];

var sitePath = window.location.pathname.slice(1, -4);
console.log(sitePath)

function setTable(data, timeFrame) {
	tbodyRef.innerHTML = "";
	console.log(data)
	var x = 1;
	for (stockData of data[timeFrame]){
		var newRow = tbodyRef.insertRow();
		var newCell1 = newRow.insertCell(0);
		var newCell2 = newRow.insertCell(1);
		var newCell3 = newRow.insertCell(2);
		var newCell4 = newRow.insertCell(3);
		var newCell5 = newRow.insertCell(4);

		newCell1.innerHTML = x;
		newCell2.innerHTML = stockData.stock;
		newCell3.innerHTML = stockData.postcount;
		newCell4.innerHTML = stockData.price;
		newCell5.innerHTML = stockData.percentchange;

		if (parseFloat(stockData.percentchange) >= 0)
		{
			newCell5.classList.add("price_positive")
		}

		else
		{
			newCell5.classList.add("price_negative")
		}

		if (x % 2 == 0)
		{
			newRow.classList.add("even_background")
		}

		x++
	}
}


async function getTableData() {
	var data_url = "https://market-popularity.herokuapp.com/" + sitePath;
	const response = await fetch(data_url, {method: "GET", mode: "cors"})
	const data = await response.json();

	day_button.style.color="blue";
	try{
		setTable(data, "day");
	} catch(error){
		tbodyRef.innerHTML = "No stock symbols found for this subreddit";
		console.error(error);
	}

	day_button.addEventListener("click", function(){
    day_button.style.color="blue";
    week_button.style.color="black";
    month_button.style.color="black";
    year_button.style.color="black";

   	setTable(data, "day");
	});

	week_button.addEventListener("click", function(){
	    day_button.style.color="black";
	    week_button.style.color="blue";
	    month_button.style.color="black";
	    year_button.style.color="black";

	    setTable(data, "week");
	});

	month_button.addEventListener("click", function(){
	    day_button.style.color="black";
	    week_button.style.color="black";
	    month_button.style.color="blue";
	    year_button.style.color="black";

	    setTable(data, "month");
	});

	year_button.addEventListener("click", function(){
	    day_button.style.color="black";
	    week_button.style.color="black";
	    month_button.style.color="black";
	    year_button.style.color="blue";

	    setTable(data, "year");
	});
}

getTableData();

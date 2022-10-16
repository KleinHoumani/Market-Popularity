var day_button = document.getElementById("day_button")
var week_button = document.getElementById("week_button")
var month_button = document.getElementById("month_button")
var year_button = document.getElementById("year_button")

day_button.addEventListener("click", function(){
    day_button.style.color="blue";
    week_button.style.color="black";
    month_button.style.color="black";
    year_button.style.color="black";
});

week_button.addEventListener("click", function(){
    day_button.style.color="black";
    week_button.style.color="blue";
    month_button.style.color="black";
    year_button.style.color="black";
});

month_button.addEventListener("click", function(){
    day_button.style.color="black";
    week_button.style.color="black";
    month_button.style.color="blue";
    year_button.style.color="black";
});

year_button.addEventListener("click", function(){
    day_button.style.color="black";
    week_button.style.color="black";
    month_button.style.color="black";
    year_button.style.color="blue";
});
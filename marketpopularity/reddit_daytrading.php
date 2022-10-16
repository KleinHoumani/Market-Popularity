<!DOCTYPE html>
<html>
<head>
	<?php include "templates/head.php" ?>
</head>
<header>
	<?php include "templates/header.php" ?>
</header>



<body id="main_body">
<h1 id="table_name">r/DayTrading</h1>
<hr id="name_separator">
<div id="time_buttons">
	<nav>
		<ul>
			<li><button id="day_button" class="time_button">Day</button></li>
			<li><button id="week_button" class="time_button">Week</button></li>
			<li><button id="month_button" class="time_button">Month</button></li>
			<li><button id="year_button" class="time_button">Year</button></li>
		</ul>
	</nav>
	<script src="/templates/nav_bar_color.js"></script>
</div>

<table id="main_table">
	<thead>
		<tr>
			<th>Rank</th>
			<th>Symbol</th>
			<th>Posts</th>
			<th>Price</th>
			<th>% Change</th>
		</tr>
	</thead>
	<tbody>
	</tbody>
</table>
<script src="/templates/set_table.js"></script>
</body>

</html>
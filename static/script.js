let chart;

async function fetchData(source) {
    const url = source === "whitepop" ? "/cities/whitepop" : `/cities/${source}`;
    console.log("Fetching from:", url); // Debug
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log("Data received:", data.slice(0, 5)); // Debug first 5
        return data;
    } catch (error) {
        console.error("Fetch error:", error);
        return [];
    }
}

function updateDashboard() {
    const source = document.getElementById("source").value;
    const attributeSelect = document.getElementById("attribute");
    const attributes = Array.from(attributeSelect.selectedOptions).map(opt => opt.value);
    const chartType = document.getElementById("chartType").value;
    const limit = parseInt(document.getElementById("limit").value);

    fetchData(source).then(data => {
        if (!data || data.length === 0) {
            console.error("No data returned for source:", source);
            return;
        }

        const isWhitePopSource = source === "whitepop";
        const adjustedData = isWhitePopSource ? data.map(city => ({
            name: city.name,
            white_pop: city.white_pop,
            population: city.white_pop, // Fallback for consistency
            white_pop_pct: 100,
            median_income: 0, // Default for missing fields
            unemployment_rate: 0
        })) : data;

        const limitedData = adjustedData.slice(0, limit);
        console.log("Limited data:", limitedData); // Debug

        // Chart
        const labels = limitedData.map(city => city.name.split(",")[0]);
        if (chart) chart.destroy();
        const ctx = document.getElementById("chart").getContext("2d");

        if (chartType === "pie" && attributes.length === 1) {
            const values = limitedData.map(city => city[attributes[0]] || 0);
            chart = new Chart(ctx, {
                type: "pie",
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#E7E9ED", "#C9CBCE", "#F7464A", "#66BB6A"]
                    }]
                },
                options: { plugins: { legend: { position: "right" } } }
            });
        } else {
            const datasets = attributes.map((attr, index) => ({
                label: attr.replace("_pct", " (%)").replace("_", " "),
                data: limitedData.map(city => city[attr] || 0),
                backgroundColor: `rgba(${(index * 100) % 255}, ${(index * 150) % 255}, ${(index * 200) % 255}, 0.2)`,
                borderColor: `rgba(${(index * 100) % 255}, ${(index * 150) % 255}, ${(index * 200) % 255}, 1)`,
                borderWidth: 1,
                fill: chartType === "line" ? false : true
            }));
            chart = new Chart(ctx, {
                type: chartType,
                data: { labels, datasets },
                options: {
                    scales: { y: { beginAtZero: true } },
                    plugins: { legend: { display: true } }
                }
            });
        }

        // Table
        const tableBody = document.getElementById("tableBody");
        tableBody.innerHTML = "";
        limitedData.forEach(city => {
            const row = document.createElement("tr");
            let cells = `<td>${city.name}</td>`;
            attributes.forEach(attr => {
                cells += `<td>${city[attr] !== undefined ? city[attr].toLocaleString() : "N/A"}</td>`;
            });
            row.innerHTML = cells;
            tableBody.appendChild(row);
        });
        const attributeHeader = document.getElementById("attributeHeader");
        attributeHeader.textContent = attributes.length > 1 ? "Attributes" : attributes[0].replace("_pct", " (%)").replace("_", " ");
        attributeHeader.colSpan = attributes.length;
    });
}

updateDashboard();
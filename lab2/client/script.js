const fetchButton = document.getElementById("fetch-button");
const cityInfoContainer = document.getElementById("city-info-container");
const cityInput = document.getElementById("city-name")

const TOKEN = "mnessel-xyz";
const CITY_INFO_ENDPOINT = "http://localhost:8000/city-info/"

var header = new Headers();
header.append("token", TOKEN);

var myInit = {
    method: "GET",
    headers: header,
    mode: "cors",
    cache: "default"
}


fetchButton.addEventListener("click", function() {
  if (cityInput.value == ''){
      window.alert("Please insert data")
      return
  }

  cityInfoContainer.innerHTML = `<img style="width: 200px" src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif?20151024034921">`

  fetch(CITY_INFO_ENDPOINT + cityInput.value, myInit)
  .then(response => {
    if (!response.ok) {
      cityInfoContainer.innerHTML = "No data available."
      window.alert("Network response was not ok: " + response);
    }
    return response.json();
  })
  .then(data => {
    if (data.error){
        window.alert(data.error)
        cityInfoContainer.innerHTML = "No data available."
        return
    }

    cityInfoContainer.innerHTML = `
      <h2>${data.name}</h2>
      <h3>Weather Months AVG (last decade)</h3>
      <table>
        <thead>
          <tr>
            <th>Month</th>
            <th>Avg temperature [℃]</th>
          </tr>
        </thead>
        <tbody>
          ${Object.entries(data.weather.months).map(([month, weather]) => `
            <tr>
              <td>${month}</td>
              <td>${weather}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
      <h3>Weather Years AVG (last decade)</h3>
      <table>
        <thead>
          <tr>
            <th>Year</th>
            <th>Avg temperature [℃]</th>
          </tr>
        </thead>
        <tbody>
          ${Object.entries(data.weather.years).map(([month, weather]) => `
            <tr>
              <td>${month}</td>
              <td>${weather}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    <br><br>
    <h3>News</h3>
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Text</th>
          <th>Author</th>
          <th>Publish Date</th>
          <th>Image</th>
        </tr>
      </thead>
      <tbody>
        ${data.news.map(item => `
          <tr>
            <td>${item.title}</td>
            <td>${item.text}</td>
            <td>${item.author}</td>
            <td>${item.publish_date}</td>
            <td><img src="${item.image}" alt="Image not available"></td>
          </tr>
        `).join("")}
      </tbody>
    </table>
    `;
  })
  .catch(error => {
     cityInfoContainer.innerHTML = "No data available."
     window.alert("Error fetching city info. ", error);
  });
});

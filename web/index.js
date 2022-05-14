let map;
const mapPin =
  "M168.3 499.2C116.1 435 0 279.4 0 192C0 85.96 85.96 0 192 0C298 0 384 85.96 384 192C384 279.4 267 435 215.7 499.2C203.4 514.5 180.6 514.5 168.3 499.2H168.3zM192 256C227.3 256 256 227.3 256 192C256 156.7 227.3 128 192 128C156.7 128 128 156.7 128 192C128 227.3 156.7 256 192 256z";

const monthRegex = new RegExp("[0-9]{4}-[0-9]{2}");
const yearRegex = new RegExp("[0-9]{4}");
const isRoot =
  window.location.href.indexOf("index.html") > 0 ||
  window.location.href.indexOf(".html") === -1;

const colorWithPriolity = [
  { priolirty: 0, order: 0, color: "#f5422a" },
  { priolirty: 6, order: 1, color: "#fd9145" },
  { priolirty: 1, order: 2, color: "#fee54a" },
  { priolirty: 7, order: 3, color: "#9de242" },
  { priolirty: 2, order: 4, color: "#72e13f" },
  { priolirty: 8, order: 5, color: "#4caf50" },
  { priolirty: 3, order: 6, color: "#64eaa9" },
  { priolirty: 9, order: 7, color: "#2be2fb" },
  { priolirty: 4, order: 8, color: "#287af4" },
  { priolirty: 10, order: 9, color: "#437cf7" },
  { priolirty: 5, order: 10, color: "#827ff8" },
  { priolirty: 11, order: 11, color: "#eb88f8" },
];

const compareOrder = (a, b) => {
  if (a.order > b.order) {
    return 1;
  }
  if (a.order < b.order) {
    return -1;
  }
};

const pickupColorList = (mapPinRangeLength) => {
  console.log(mapPinRangeLength);
  if (mapPinRangeLength === 1) return [colorWithPriolity[0].color];
  return (colorList = colorWithPriolity
    .filter((x) => x.priolirty < mapPinRangeLength)
    .sort(compareOrder)
    .map((x) => x.color));
};

class MapPinGenerationFailError extends Error {
  constructor(message) {
    super(message);
    this.name = "MapPinGenerationFailError";
  }
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 2,
    center: new google.maps.LatLng(2.8, -187.3),
    mapTypeId: "terrain",
  });

  // Create a <script> tag and set the USGS URL as the source.
  const script = document.createElement("script");

  const query = window.location.href.split("?")[1];

  // This example uses a local copy of the GeoJSON stored at
  // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
  if (!query) {
    script.src = "data/data.js";
  } else {
    const name = query.replace("data=", "");
    script.src = `data/${name}.js`;
  }
  document.getElementsByTagName("head")[0].appendChild(script);
  if (!isRoot) {
    toggleButtonControl();
    constructLinkGenerator();
    handleInput();
  }
}

const chooseColor = (freq, distColorList) => {
  for (let distColor of distColorList) {
    if (distColor.min <= freq && freq <= distColor.max) {
      return distColor.color;
    }
  }
};

const generateEmptyRangeList = (color_num) => {
  return (range_list = [...Array(color_num)].reduce(
    (_rangeList, _) => [..._rangeList, [0, 0]],
    []
  ));
};

const doesNotHaveEmptyElement = (range_list) => {
  return range_list.reduce((_isFull, range) => {
    const [x1, x2] = range;
    _isFull &= x1 !== 0 && x2 !== 0;
    return _isFull;
  }, true);
};

const generateMapPinRange = (data) => {
  if (data.length === 1) {
    return [[data[0][2], data[0][2]]];
  }
  const freqencyCountObject = data.reduce((freqencyCountObject, datum) => {
    const freqency = datum[2];

    if (!freqencyCountObject[freqency]) {
      freqencyCountObject[freqency] = 1;
      return freqencyCountObject;
    } else {
      ++freqencyCountObject[freqency];
      return freqencyCountObject;
    }
  }, {});

  const master_color_num = 12;

  for (let color_num of [...Array(master_color_num + 1).keys()].reverse()) {
    if (color_num === 0) {
      throw new MapPinGenerationFailError(
        "Map Pin range generation failed. Check out input data"
      );
    }

    let total = data.length;
    let criterion_num = Math.floor(total / color_num);
    let range_list_index = 0;
    let min_max_index = 0;

    const range_list = Object.entries(freqencyCountObject).reduce(
      (_rangeList, freqencyCount) => {
        if (!_rangeList) {
          throw new MapPinGenerationFailError(
            "Map Pin range generation failed. Check out input data"
          );
        }
        const [frequency, count] = freqencyCount;
        if (criterion_num > 0) {
          if (min_max_index === 0) {
            _rangeList[range_list_index][min_max_index] = frequency;
            total = total - count;
            criterion_num = criterion_num - count;
            min_max_index = 1;
            return _rangeList;
          } else {
            total = total - count;
            criterion_num = criterion_num - count;
            _rangeList[range_list_index][min_max_index] = frequency;
            return _rangeList;
          }
        } else {
          _rangeList[range_list_index][min_max_index] = frequency;
          min_max_index = 0;
          range_list_index = range_list_index + 1;
          _rangeList[range_list_index][min_max_index] = frequency;
          total = total - count;
          color_num = color_num - 1;
          criterion_num = Math.floor(total / color_num);
          if (criterion_num === 0) criterion_num = 1;
          return _rangeList;
        }
      },
      generateEmptyRangeList(color_num)
    );

    if (doesNotHaveEmptyElement(range_list)) return range_list;
  }
};

const generateLegend = (distColorList) => {
  const legend = document.getElementById("legend");
  const outerDiv = document.createElement("div");

  for (var distColor of distColorList) {
    const colorContainer = document.createElement("div");
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    const span = document.createElement("span");
    const text = document.createTextNode(distColor.min + " - " + distColor.max);
    span.appendChild(text);
    svg.setAttribute("viewBox", "0 0 600 600");
    svg.setAttribute("width", "25");
    svg.setAttribute("height", "25");
    path.setAttribute("fill", distColor.color);
    path.setAttribute("d", mapPin);
    svg.appendChild(path);
    colorContainer.appendChild(svg);
    colorContainer.appendChild(span);
    colorContainer.setAttribute("class", "color-container");
    outerDiv.appendChild(colorContainer);
  }
  legend.appendChild(outerDiv);
};

const editgenelateLink = () => {
  const legend = document.getElementById("legend");
  const genelateLinkContainer = document.getElementById("generate-link");
  legend.appendChild(genelateLinkContainer);
};

const toggleButtonControl = () => {
  const toggle = document.getElementById("switch");
  toggle.addEventListener("click", () => switchInputMode());
};

const isValidQuery = (inputData) => {
  return !monthRegex.test(inputData) && !yearRegex.test(inputData);
};

const generateLink = (inputData) => {
  const prevLink = document.getElementById("link");
  if (prevLink) {
    prevLink.parentElement.removeChild(prevLink);
  }
  const genelateLinkContainer = document.getElementById("generate-link");
  const linkP = document.createElement("p");
  const linkA = document.createElement("a");
  const query = window.location.href.split("?")[0];
  const link = isValidQuery(inputData) ? query : `${query}?data=${inputData}`;
  const linkText = document.createTextNode(
    isValidQuery(inputData) ? "All" : inputData
  );
  linkA.appendChild(linkText);
  linkA.setAttribute("href", link);
  linkP.appendChild(linkA);
  linkP.setAttribute("id", "link");
  genelateLinkContainer.appendChild(linkP);
};

const constructLinkGenerator = () => {
  const START_YEAR = 2020;
  const today = new Date();
  const thisYearYyyy = today.getFullYear();
  const nextYearYyyy = parseInt(thisYearYyyy) + 1;
  const yearOptionArray = [...new Array(nextYearYyyy - START_YEAR).keys()]
    .map((i) => String(START_YEAR + i))
    .reduce((_yearOptionArray, year) => {
      const option = document.createElement("option");
      const yearText = document.createTextNode(year);
      option.appendChild(yearText);
      _yearOptionArray.push(option);
      return _yearOptionArray;
    }, []);

  const year = document.getElementById("year-select");
  for (let yearOption of yearOptionArray) {
    year.appendChild(yearOption);
  }

  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const thisMonth = `${thisYearYyyy}-${mm}`;
  const month = document.getElementById("month-select");
  month.setAttribute("max", thisMonth);
};

const handleInput = () => {
  const year = document.getElementById("year-select");
  const month = document.getElementById("month-select");
  year.addEventListener("input", () =>
    generateLink(year.options[year.selectedIndex].textContent)
  );
  month.addEventListener("input", (e) => generateLink(e.target.value));
};

const switchInputMode = () => {
  const label = document.getElementById("toggle-label");
  const year = document.getElementById("year-link");
  const month = document.getElementById("month-link");
  let text = label.textContent;
  label.textContent = text === "Year" ? "Month" : "Year";
  if (text === "Year") {
    year.setAttribute("hidden", "hidden");
    month.removeAttribute("hidden");
  } else {
    month.setAttribute("hidden", "hidden");
    year.removeAttribute("hidden");
  }
};

class EventControl {
  constructor() {
    this.current;
  }
}
// Loop through the res array and place a marker for each
// set of coordinates.
const geo_call = function (data) {
  let svgMarker = {
    path: mapPin,
    fillColor: "",
    fillOpacity: 1,
    strokeWeight: 0,
    rotation: 0,
    scale: 0.05,
    anchor: new google.maps.Point(194, 512),
  };

  const mapPinRange = generateMapPinRange(data);
  const colorList = pickupColorList(mapPinRange.length);
  const distColorList = mapPinRange.reduce((_dictColorList, range, i) => {
    _dictColorList.push({
      min: parseInt(range[0]),
      max: parseInt(range[1]),
      color: colorList[i],
    });
    return _dictColorList;
  }, []);

  for (datum of data) {
    const latLng = new google.maps.LatLng(Number(datum[0]), Number(datum[1]));
    svgMarker.fillColor = chooseColor(datum[2], distColorList);

    const content = `
    <div>
    <p>${datum[2]}</p>
    <dr>
    <p>Latitude: ${datum[0]}</p>
    <p>Longitude: ${datum[1]}</p>
    </div>
    `;

    const infowindow = new google.maps.InfoWindow({
      content: content,
    });

    const marker = new google.maps.Marker({
      position: latLng,
      icon: svgMarker,
      map: map,
    });

    marker.addListener("click", () => {
      infowindow.open({
        anchor: marker,
        map,
        shouldFocus: false,
      });
    });
  }
  generateLegend(distColorList);
  if (!isRoot) editgenelateLink();
};

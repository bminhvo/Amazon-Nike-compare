(function() {
  'use strict';

  angular
    .module('compareApp')
    .controller('CompareCtrl', CompareCtrl);


  CompareCtrl.$inject = ['$state', '$http', '$timeout', '$mdToast'];
  function CompareCtrl($state, $http, $timeout, $mdToast) {
    var vm = this;
    vm.submitForm = submitForm;

    vm.error = false;

    vm.website = false;
    vm.activated = false;

    console.log(vm.keyword);

    function submitForm(keyword) {
      clearBox('barDiv')
      vm.error = false;
      vm.activated = true;
      console.log(keyword);
      $http
        .post('/', vm.keyword)
        .then(function(response) {
          console.log(response);
          vm.results = response.data;
        }, function(error) {
          console.log(error);
          vm.error = error;
          vm.website = false;
          vm.activated = false;
        })
        .then(function(response) {

          $http
            .get("/static/js/amazon-output.json")
            .then(function(response) {
              vm.data = response.data;
              vm.items = vm.data.items;
              console.log(typeof response);
              console.log(typeof vm.items);
              vm.activated = false;
              vm.website = true;
            });


          $http
            .get("/static/js/nike-output.json")
            .then(function(response) {
              vm.datan = response.data;
              vm.itemsn = vm.datan.items;
              console.log(typeof response);
              console.log(typeof vm.itemsn);
            });

          $http
            .get("/static/js/amazon-average.json")
            .then(function(response) {
              vm.averagesA = response.data;
              console.log(response);
            });

          $http
            .get("/static/js/nike-average.json")
            .then(function(response) {
              vm.averagesN = response.data;
              drawBar();
            });

        }); //End of post request

        vm.keyword = "";
        if(vm.website){
          showToast();
        }
    };

    // To clear the bar for re-searching
    function clearBox(elementID) {
      document.getElementById(elementID).innerHTML = "";
    }


    // Use D3 to draw bar
    function drawBar() {
      // set the dimensions of the canvas
      var margin = {top: 20, right: 20, bottom: 70, left: 40},
          width = 400 - margin.left - margin.right,
          height = 450 - margin.top - margin.bottom;
      // set the ranges
      var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
      var y = d3.scale.linear().range([height, 0]);
      // define the axis
      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom")
      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left")
          .ticks(10);
      // add the SVG element
      var svg = d3.select("#barDiv").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
      // load the data
      d3.json("/static/js/nike-bar.json", function(error, data) {
        console.log(data);
        data.forEach(function(d) {
            d.Category = d.Category;
            d.Price = +d.Price;
        });
        // scale the range of the data
        x.domain(data.map(function(d) { return d.Category; }));
        y.domain([0, d3.max(data, function(d) { return d.Price; })]);
        // add axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
          .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", "-.55em")
            .attr("transform", "rotate(-90)" );
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 5)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Price");
        // Add bar chart
        svg.selectAll("bar")
            .data(data)
          .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.Category); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.Price); })
            .attr("height", function(d) { return height - y(d.Price); });
      });
    } // End of drawBar()


    function showToast(){
      console.log("showToast!!!!")
      var last = {
          bottom: true,
          top: false,
          left: false,
          right: true
        };
      vm.toastPosition = angular.extend({},last);
      vm.getToastPosition = function() {
        sanitizePosition();
        return Object.keys(vm.toastPosition)
          .filter(function(pos) { return vm.toastPosition[pos]; })
          .join(' ');
      };
      function sanitizePosition() {
        var current = vm.toastPosition;
        if ( current.bottom && last.top ) current.top = false;
        if ( current.top && last.bottom ) current.bottom = false;
        if ( current.right && last.left ) current.left = false;
        if ( current.left && last.right ) current.right = false;
        last = angular.extend({},current);
      }
      vm.showSimpleToast = function() {
        var pinTo = vm.getToastPosition();
        $mdToast.show(
          $mdToast.simple()
            .textContent('Keep seeing the same results? Open the developer tools (Ctrl+Shift+i) and reload.')
            .position(pinTo )
            .hideDelay(2000)
        );
      };
      vm.showSimpleToast();
    }



  } // End of controller
})();

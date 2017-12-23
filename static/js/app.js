(function() {
  'use strict';

  angular.module('compareApp', [
    // Angular modules
    'ui.router',
    'ngAnimate',
    'ngMaterial',
  ])
  .config(configFunction)


  configFunction.$inject = ['$stateProvider', '$urlRouterProvider'];
  function configFunction($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider
    .state('home', {
      url: '/',
      templateUrl: '/static/partials/home.html',
      controller: 'CompareCtrl',
      controllerAs: 'vm'
      })

      .state('about', {
        url: '/about',
        templateUrl: '../static/partials/about.html',
      });

  }
})();

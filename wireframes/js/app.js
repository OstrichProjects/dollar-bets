var App = Ember.Application.create()

App.ApplicationAdapter = DS.DjangoRESTAdapter.extend({});

App.Router.map(function () {
	this.resource('index', {path: '/'})
})
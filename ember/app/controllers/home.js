import Ember from 'ember';

export default Ember.Controller.extend({
  ctf: null,
  html: '',
  set_html: function(){
    var ctf = this.get('ctf');
    if(ctf){
      var t = this;
      this.store.findRecord('home', ctf.get('id')).then(function(home) {
        if(home){
          t.set('html', home.get('html'));
        }
      });
    }
  }.observes('ctf').on('init'),
});

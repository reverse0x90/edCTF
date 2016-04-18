import Ember from 'ember';

export default Ember.Controller.extend({
  ctf: null,
  html: '',
  set_html: function(){
    var ctf = this.get('ctf');
    if(ctf){
      var t = this;
      this.store.findRecord('about', ctf.get('id')).then(function(about) {
        if(about){
          t.set('html', about.get('html'));
        }
      });
    }
  }.observes('ctf').on('init'),
});

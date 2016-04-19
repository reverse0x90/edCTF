import Ember from 'ember';

export default Ember.Controller.extend({
  ctf: null,
  html: '',
  set_html: function(){
    var ctf = this.get('ctf');
    if(ctf){
      var t = this;
      ctf.get('home').then(function(home){
        t.set('html', home.get('html'));
      });
    }
  }.observes('ctf').on('init'),
});

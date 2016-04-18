import Ember from 'ember';

export default Ember.Controller.extend({
  ctf: null,
  html: '',
  set_html: function(){
    var ctf = this.get('ctf');
    if(ctf){
      var t = this;
      ctf.get('about').then(function(about){
        t.set('html', about.get('html'));
      });
    }
  }.observes('ctf').on('init'),
});

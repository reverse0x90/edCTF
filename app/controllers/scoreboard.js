import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: undefined,
  options: undefined,
  setOptions: function(){
    var options = {
      width: 1000,
      height: this.get('ctf.scoreboard.numtopteams')*34,
      vAxis: {
        format: 'decimal',
      },
      hAxis: {
        maxTextLines: 100,
      },
      //selectionMode: 'multiple',
    };
    this.set('options', options);
  }.observes('ctf.scoreboard.numtopteams').on('init'),
  actions:{
    openTeamView: function(id){
      this.store.find('team', id).then((team) => {
        this.set('modal.team', team);
      });
      this.set('modal.isTeam', true);
    }
  },
});

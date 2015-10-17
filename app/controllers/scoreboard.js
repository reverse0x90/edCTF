import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: undefined,
  options: {
    lineWidth: 0,
    width: 900,
    height: 500,
    //selectionMode: 'multiple',
  },
  actions:{
    openTeamView: function(id){
      this.store.find('team', id).then((team) => {
        this.set('modal.team', team);
      });
      this.set('modal.isTeam', true);
    }
  },
});

import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  htmlPage: null,
  pageName: '',

  set_pageName: function(){
    const htmlPage = this.get('htmlPage');
    if(htmlPage){
      const t = this;
      htmlPage.then(function(htmlPage){
        t.set('pageName', htmlPage.get('constructor.modelName'));
      });
    }
  }.observes('htmlPage').on('init'),

  actions: {
    editAdminHtml: function(){
      let t = this;
      let htmlPage = this.get('htmlPage');
      if(htmlPage){
        htmlPage.then(function(htmlPage){
          htmlPage.save().then(function(){
            t.set('modal.isAdminHtml', false);
            t.set('modal.htmlPage', null);
            t.set('modal.errorMessage', '');
            t.set('modal.errorFields', {});  
          }, function(err){
            htmlPage.rollbackAttributes();
            if (err.errors.message){
              t.set('modal.errorMessage', err.errors.message);
              t.set('modal.errorFields', err.errors.fields);
            } else {
              t.set('modal.errorMessage', 'Server error, unable to edit page');
              t.set('modal.errorFields', {});
            }
          });
        });
      }
    },
    closeAdminHtmlModal: function() {
      this.set('modal.isAdminHtml', false);
      this.set('modal.htmlPage', null);
      this.set('modal.errorMessage', '');
      this.set('modal.errorFields', {});

      let htmlPage = this.get('htmlPage');
      if (htmlPage){
        htmlPage.then(function(htmlPage){
          htmlPage.rollbackAttributes();
        });
      }
    },
  }
});

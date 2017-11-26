 function preprocess_and_glm(subject, session)
  %subject is SID, session is Pre or Post as string
  [g,s] = modGLM(subject, session);
  groovy_realign(g,s)
  coax_fieldmap(subject, session);
  groovy_subject_model(g,s)
  groovy_contrasts(g,s)
end

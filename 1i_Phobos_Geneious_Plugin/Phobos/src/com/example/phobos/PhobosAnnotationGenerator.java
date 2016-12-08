package com.example.phobos;

import com.biomatters.geneious.publicapi.plugin.DocumentSelectionSignature;
import com.biomatters.geneious.publicapi.plugin.GeneiousActionOptions;
import com.biomatters.geneious.publicapi.plugin.SequenceAnnotationGenerator;

public class PhobosAnnotationGenerator extends SequenceAnnotationGenerator {
	
	static final String HELP = "Phobos detects tandem repeats in DNA sequences(s)";

	@Override
	public GeneiousActionOptions getActionOptions() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String getHelp() {
		return HELP;
	}

	@Override
	public DocumentSelectionSignature[] getSelectionSignatures() {
		// TODO Auto-generated method stub
		return null;
	}

}

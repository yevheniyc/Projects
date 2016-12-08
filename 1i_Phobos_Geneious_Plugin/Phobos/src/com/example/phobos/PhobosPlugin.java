package com.example.phobos;

import com.biomatters.geneious.publicapi.plugin.GeneiousPlugin;
import com.biomatters.geneious.publicapi.plugin.SequenceAnnotationGenerator;

/**
 * This plugin shows how to create a simple annotation generator plugin. This allows
 * the user to create annotations that appear in the sequence viewer.
 * <p/>
 * A few lines of code cause a menu entry to appear in the tools drop-down menu in the sequence viewer.
 * Upon selecting it a dialog populated with various options appears. Finally all the
 * code in this plugin has to do, is given a sequence return a list of annotations to be
 * added to the sequence and the Geneious framework handles the rest (such as saving
 * to disk, providing undo functionality, laying out the options GUI, remembering user
 * selected option values between invocations).
 * <p/>
 * This class just provides the framework to hook the {@link com.example.phobos.Phobos}
 * into Geneious. All of the real work happens in {@link com.example.phobos.Phobos}.
 */
public class PhobosPlugin extends GeneiousPlugin {
    public SequenceAnnotationGenerator[] getSequenceAnnotationGenerators() {
        return new SequenceAnnotationGenerator[]{
                new PhobosAnnotationGenerator()
        };
    }

    public String getName() {
        return "Phobos Tandem Repeat Finder";
    }

    public String getHelp() {
        return PhobosAnnotationGenerator.HELP;
    }

    public String getDescription() {
        return "DNA-satellite search tool";
    }

    public String getAuthors() {
        return "Yev";
    }

    public String getVersion() {
        return "0.1";
    }

    public String getMinimumApiVersion() {
        return "4.1";
    }

    public int getMaximumApiVersion() {
        return 4;
    }
}

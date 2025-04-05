? This is a NEURON mod file generated from a ChannelML file

? Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: NaChannel

COMMENT
    Simple example of Na conductance in squid giant axon. Based on channel from Hodgkin and Huxley 1952
ENDCOMMENT

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
    (um) = (micrometer)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (l) = (liter)
}


NEURON {
	SUFFIX kdrin
	USEION k READ ki, ko WRITE ik
	RANGE gkdrbar, ik, gk
	
}

<!-- UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)	
} -->

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}
PARAMETER {
	v (mV)
	dt (ms)
	gkdrbar= 0.0338 (mho/cm2) <0,1e9>
	
	
}

STATE {
	n
}

ASSIGNED {
	ik (mA/cm2)
	inf
	tau (ms)
	gk (mho/cm2)
	ek (mV)
	ki (mM)
	ko (mM)

}


INITIAL {
	rate(v)
	n = inf
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	gk= gkdrbar*n*n*n*n
	ek = 25 * (log(ko/ki))
	ik = gk*(v-ek)
	
}

DERIVATIVE states {
	rate(v)
	n' = (inf-n)/tau
}

UNITSOFF

FUNCTION alf(v){ 
	LOCAL va 
	
	va=v-13
	if (fabs(va)<1e-04){
	   va=va+0.0001
		alf= (-0.018*va)/(-1+exp(-(va/25)))
	} else {
	  	alf = (-0.018*(v-13))/(-1+exp(-((v-13)/25)))
	}
}


FUNCTION beta(v) { 
	
	LOCAL vb 
	
	vb=v-23
	if (fabs(vb)<1e-04){
	  vb=vb+0.0001
		bet= (0.0054*vb)/(-1+exp(vb/12))
	} else {
	  	bet = (0.0054*(v-23))/(-1+exp((v-23)/12))
	}
}	




PROCEDURE rate(v (mV)) {
    LOCAL alpha, beta, sum, eps1, eps2
    TABLE ninf, tau DEPEND celsius FROM -100 TO 100 WITH 400
    UNITSOFF

    // Compute a small correction if v-13 (or v-23) is near zero:
    eps1 = (fabs(v - 13) < 1e-4) ? 1e-4 : 0
    eps2 = (fabs(v - 23) < 1e-4) ? 1e-4 : 0

    // Calculate alpha and beta using the adjusted values:
    alpha = (-0.018 * ((v - 13) + eps1)) / (-1 + exp(-(((v - 13) + eps1)/25)))
    beta  = (0.0054 * ((v - 23) + eps2))  / (-1 + exp(((v - 23) + eps2)/12))

    sum = alpha + beta
    ninf = alpha / sum
    tau = 1 / sum

    UNITSON
}

UNITSON	




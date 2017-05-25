CC=icc
FC=ifort
AR=ar
FFLAGS=-fPIC -O3
ARFLAGS         =      ru
INCLUDES = -I/usr/local/netcdf_with_hdf/include

F2PY_FLAGS= -I./ -I/usr/local/netcdf_with_hdf/include 

SRCS = cs_stat.f90 

F2PY = f2py
OBJS = $(SRCS:.f90=.o)
MODULE =cs_stat
all:    ${MODULE}.so
	@echo  ${MODULE}.so has been compiled

${MODULE}.so: ${MODULE}.f90 libpost.a #$(OBJS)
	$(F2PY) $(F2PY_FLAGS) --fcompiler=intelem --f90flags=-fPIC -L/usr/local/netcdf_with_hdf/lib -lnetcdff -lnetcdf  -m ${MODULE} -c $< #$(OBJS) #${MODULE}.F90 

libpost.a: $(OBJS)
	$(AR) ru libpost.a $(OBJS) 


# this is a suffix replacement rule for building .o's from .c's
# it uses automatic variables $<: the name of the prerequisite of
# the rule(a .c file) and $@: the name of the target of the rule (a .o file) 
# (see the gnu make manual section about automatic variables)
#.F90.o:
#	$(FC) $(FFLAGS) $(INCLUDES) -c $<  -o $@
%.o: %.f90
	$(RM) $@
	$(FC) $(FFLAGS) -o $@ -c $(INCLUDES) $(FCSUFFIX) $*.f90

cs_stat.o: 

clean:
	$(RM) *.a *.pyc *.o *.mod  $(MODULE).so

#depend: $(SRCS)
#	makedepend $(INCLUDES) $^


# DO NOT DELETE THIS LINE -- make depend needs it

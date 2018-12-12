DOCUMENTROOT=$(DESTDIR)/etc/elphel393
OWN = -o root -g root
INSTDOCS = 0644
INSTALL = install
DOCS =      ros2_client.py \
            ros2_config.py \
            ros2_config.xml \
            ros2_init.py \
            ros2_master.py \
            ros2_slave.py

all:
	@echo "make all in src"

install:
	@echo "make install in src"
	$(INSTALL) $(OWN) -d $(DOCUMENTROOT)
	$(INSTALL) $(OWN) -m $(INSTDOCS) $(DOCS) $(DOCUMENTROOT)

clean:
	@echo "make clean in src"

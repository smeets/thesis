
.PHONY: report

report:
	$(MAKE) report -C report
	cp report/out/report.pdf .

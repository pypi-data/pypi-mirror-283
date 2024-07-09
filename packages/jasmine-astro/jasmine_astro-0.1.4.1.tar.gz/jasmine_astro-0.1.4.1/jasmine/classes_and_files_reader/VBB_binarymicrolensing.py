import VBBinaryLensing
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class VBBandRTModelTemplateForBinaryLightCurve():
    """
    Generate a light curve based on a line of RTModel template
    """
    template_line: int
    separation_s: float
    mass_ratio_q: float
    impact_parameter_u0: float
    angle_alpha: float
    source_radius_rho: float
    pre_calculated_peak_tp1: float
    pre_calculated_peak_tp2: float
    einstein_time_tE: float
    peak_time_t0: float

    def __init__(self, *, template_line, path_to_template,
                 input_tE, input_t0, cadence_in_days):

        vbb = VBBinaryLensing.VBBinaryLensing()
        self.path_to_template = path_to_template
        line_information = read_template(path_to_template).loc[template_line - 2]
        self.separation_s = line_information['s']
        self.mass_ratio_q = line_information['q']
        self.impact_parameter_u0 = line_information['u0']
        self.angle_alpha = line_information['alpha']
        self.source_radius_rho = line_information['rho']
        self.einstein_time_tE = input_tE
        self.peak_time_t0 = input_t0
        self.cadence = cadence_in_days
        time_interval = np.arange(start=self.peak_time_t0 - 2 * self.einstein_time_tE,
                                  stop=self.peak_time_t0 + 2 * self.einstein_time_tE,
                                  step=self.cadence)
        pr = [np.log(self.separation_s), np.log(self.mass_ratio_q),
              self.impact_parameter_u0, self.angle_alpha,
              np.log(self.source_radius_rho), np.log(self.einstein_time_tE), self.peak_time_t0]
        self.results = vbb.BinaryLightCurve(pr, time_interval)
        self.times = time_interval
        self.magnification = self.results[0]


def read_template(path_to_template):
    template_df = pd.read_csv(path_to_template,
                              skiprows=1,
                              sep=r'\s+',
                              names=['s', 'q', 'u0', 'alpha', 'rho', 'tp1', 'tp2'],
                              )
    return template_df

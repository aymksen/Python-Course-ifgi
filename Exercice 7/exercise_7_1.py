# -*- coding: utf-8 -*-
"""QGIS Processing script: Create City District Profile
Layers needed:
  Muenster_City_Districts   
  House_Numbers             
  Muenster_Parcels          
  Schools                   
  public_swimming_pools     
"""

from qgis.PyQt.QtCore import QCoreApplication, QSize
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.core import (
    QgsProject, QgsProcessingAlgorithm, QgsProcessingException,
    QgsProcessingParameterEnum, QgsProcessingParameterFileDestination,
    QgsSpatialIndex, QgsFeatureRequest, QgsMapSettings, QgsMapRendererCustomPainterJob
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
import os, tempfile, math


class CreateCityDistrictProfile(QgsProcessingAlgorithm):
    DISTRICT, DATASET, OUTPUT = 'DISTRICT', 'DATASET', 'OUTPUT'

    # metadata
    def name(self):        return 'create_city_district_profile'
    def displayName(self): return self.tr('Create City District Profile')
    def group(self):       return self.tr('Workshop Scripts')
    def groupId(self):     return 'workshopScripts'
    def shortHelpString(self):
        return self.tr('Generate a PDF report (with vector map) for one city district.')

    # parameters
    def initAlgorithm(self, _config=None):
        self._district_names = self._list_districts()
        self.addParameter(QgsProcessingParameterEnum(self.DISTRICT, 'City district',
                                                     options=self._district_names))
        self.addParameter(QgsProcessingParameterEnum(self.DATASET, 'Statistics about',
                                                     options=['Schools', 'Swimming Pools']))
        self.addParameter(QgsProcessingParameterFileDestination(
            self.OUTPUT, 'Output PDF', fileFilter='PDF files (*.pdf)'))

    # entry point
    def processAlgorithm(self, params, context, _feedback):
        dist_idx = self.parameterAsEnum(params, self.DISTRICT, context)
        choice   = self.parameterAsEnum(params, self.DATASET, context)
        pdf_path = self.parameterAsFile(params, self.OUTPUT, context)
        name     = self._district_names[dist_idx]

        lyr      = self._layers()
        stats    = self._statistics(name, choice, lyr)
        png_path = self._render_map(name, choice, lyr)
        self._build_pdf(pdf_path, name, choice, stats, png_path)
        return {self.OUTPUT: pdf_path}

    # helpers
    def _list_districts(self):
        l = QgsProject.instance().mapLayersByName('Muenster_City_Districts')
        if not l:
            raise QgsProcessingException('Layer "Muenster_City_Districts" missing.')
        return sorted({f['Name'] for f in l[0].getFeatures()})

    def _layers(self):
        def get(name):
            l = QgsProject.instance().mapLayersByName(name)
            if not l:
                raise QgsProcessingException(f'Layer "{name}" missing.')
            return l[0]
        return {
            'districts':  get('Muenster_City_Districts'),
            'households': get('House_Numbers'),
            'parcels':    get('Muenster_Parcels'),
            'schools':    get('Schools'),
            'pools':      get('public_swimming_pools')
        }

    def _statistics(self, name, choice, lyr):
        expr = f"\"Name\" = '{name.replace("'", "''")}'"
        district = next(lyr['districts'].getFeatures(QgsFeatureRequest().setFilterExpression(expr)), None)
        if not district:
            raise QgsProcessingException(f'District "{name}" not found.')
        geom = district.geometry()

        def count_points(layer):
            idx = QgsSpatialIndex(layer.getFeatures())
            return sum(1 for fid in idx.intersects(geom.boundingBox())
                       if layer.getFeature(fid).geometry().within(geom))

        households = count_points(lyr['households'])
        tgt_lyr    = lyr['schools'] if choice == 0 else lyr['pools']
        targets    = count_points(tgt_lyr)

        idx_par    = QgsSpatialIndex(lyr['parcels'].getFeatures())
        parcels    = sum(1 for fid in idx_par.intersects(geom.boundingBox())
                         if lyr['parcels'].getFeature(fid).geometry().intersects(geom))

        return dict(parent=district['P_District'],
                    area=geom.area(),
                    households=households,
                    parcels=parcels,
                    target=targets,
                    geom=geom)

    def _render_map(self, name, choice, lyr):
        geom = self._statistics(name, choice, lyr)['geom']  # geometry for extent
        bbox = geom.buffer(geom.length() * 0.05, 5).boundingBox()

        # draw district first (bottom), then parcels, then points
        layers_to_draw = [lyr['districts'], lyr['parcels'], lyr['households']]
        layers_to_draw.append(lyr['schools'] if choice == 0 else lyr['pools'])

        ms = QgsMapSettings()
        ms.setLayers(layers_to_draw)
        ms.setExtent(bbox)
        ms.setOutputSize(QSize(1800, 1800))
        ms.setOutputDpi(300)

        img = QImage(ms.outputSize(), QImage.Format_ARGB32_Premultiplied)
        img.fill(0xFFFFFFFF)
        p = QPainter(img)
        QgsMapRendererCustomPainterJob(ms, p).renderSynchronously()
        p.end()

        png = os.path.join(tempfile.gettempdir(), f"{name.replace(' ', '_')}_map.png")
        img.save(png, 'PNG')
        return png

    def _build_pdf(self, path, name, choice, s, png):
        doc = SimpleDocTemplate(path, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)
        st  = getSampleStyleSheet()
        flow = [Paragraph(f'<b>{name}</b>', st['Title']), Spacer(1, 6*mm)]

        img = RLImage(png)
        img._restrictSize(130*mm, 160*mm)  # keep image within page
        flow.append(img)
        flow.append(Spacer(1, 6*mm))

        flow += [Paragraph(f'Parent district: {s["parent"]}', st['Normal']),
                 Paragraph(f'Area: {s["area"]/1_000_000:.2f} km²', st['Normal']),
                 Paragraph(f'Households: {s["households"]}', st['Normal']),
                 Paragraph(f'Parcels: {s["parcels"]}', st['Normal'])]

        label = 'Schools' if choice == 0 else 'Swimming pools'
        flow.append(Paragraph(f'{label}: {s["target"]}' if s['target'] else f'No {label.lower()} in this district.',
                              st['Normal']))

        doc.build(flow)

    # Qt translation helper
    def tr(self, text):
        return QCoreApplication.translate('CreateCityDistrictProfile', text)

    def createInstance(self):
        return CreateCityDistrictProfile()

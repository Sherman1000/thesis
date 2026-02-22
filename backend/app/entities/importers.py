from app.models.authomatic_corrections import AuthomaticCorrection


class AuthomaticCorrectionImporter:
    def import_corrections(self, correction_requests):
        authomatic_corrections = []
        for correction_request in correction_requests:
            authomatic_correction = AuthomaticCorrection.from_request(correction_request)
            authomatic_corrections.append(authomatic_correction)

        AuthomaticCorrection.objects.bulk_create(authomatic_corrections)

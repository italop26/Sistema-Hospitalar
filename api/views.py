from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ConsultaSerializer, ExameSerializer
from .services.consulta_service import ConsultaService
from .services.exames_service import ExameService


class ConsultaAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ConsultaSerializer(
            data=request.data['data']
        )

        serializer.is_valid(raise_exception=True)

        try:

            consulta = ConsultaService.criar_consulta(
                paciente=request.user.paciente,
                especialidade=serializer.validated_data[
                    "especialidade"
                ],
                data_consulta=serializer.validated_data[
                    "data_consulta"
                ],
            )

        except ValueError as erro:

            return Response(
                {"erro": str(erro)},
                status=status.HTTP_400_BAD_REQUEST
            )

        resposta = ConsultaSerializer(consulta)

        return Response(
            resposta.data,
            status=status.HTTP_201_CREATED
        )


class ExameAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ExameSerializer(
            data=request.data['data']
        )

        serializer.is_valid(raise_exception=True)

        try:

            exame = ExameService.criar_exame(
                paciente=request.user.paciente,
                especialidade=serializer.validated_data[
                    "especialidade"
                ],
                data=serializer.validated_data[
                    "data"
                ],
            )

        except ValueError as erro:

            return Response(
                {"erro": str(erro)},
                status=status.HTTP_400_BAD_REQUEST
            )

        resposta = ExameSerializer(exame)

        return Response(
            resposta.data,
            status=status.HTTP_201_CREATED
        )
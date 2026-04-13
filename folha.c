#include <stdio.h>

int main()
{
    
    float salario, inss, irrf, irrf_deducao, deducao_inss, liquido, desconto_vt, desconto_vr;
    
    inss = 0;
    irrf = 0;
    irrf_deducao = 0;
    deducao_inss = 0;
    
    printf("Digite o seu salário: R$ ");
    scanf("%f", &salario);
    printf("Desconto de Vale Refeição: R$ ");
    scanf("%f", &desconto_vr);

    
    if (salario <= 1621) {
        inss = 0.075;
        deducao_inss = 0;
    } else {
        if (salario >= 1621.01 && salario < 2902.84) {
            inss = 0.09;
            deducao_inss = 24.31500;
        } else {
            if (salario >= 2902.84 && salario < 4354.27) {
                inss = 0.12;
                deducao_inss = 111.40020;
            } else {
                if (salario >= 4354.27 && salario < 8475.55) {
                    inss = 0.14;
                    deducao_inss = 198.48560;
                } else {
                    if (salario >= 8475.55) {
                        inss = 0.14;
                        deducao_inss = 0;
                    }
                }
            }
        }
    }

    float desconto_inss = (salario * inss) - deducao_inss;

    if (desconto_inss > 951.64) {
        desconto_inss = 951.64;
    }
    
    if (salario >= 5000.00 && salario < 7350.01) {
        irrf = ((salario - inss) * 0.275) - 908.73;
        irrf_deducao = 978.62 - (0.133145 * salario);
    } else {
        if (salario >= 7350.01) {
            irrf = ((salario - inss) * 0.275) - 908.73;
        }
    }

    desconto_vt = salario * 0.06;
    
    printf("O desconto de inss foi de R$ %.2f\n", desconto_inss);
    printf("O desconto de irrf foi de R$ %.2f\n", irrf - irrf_deducao);
    printf("O desconto de Vale Transporte foi de : R$ %.2f\n", desconto_vt);
    
    liquido = salario - desconto_inss - (irrf - irrf_deducao) - (desconto_vt - desconto_vr);

    printf("\nO salário final é: R$ %.2f", liquido);

    return 0;
    
}

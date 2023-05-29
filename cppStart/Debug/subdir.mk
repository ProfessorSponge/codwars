################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../Kata20203315.cpp \
../helloThere.cpp 

CPP_DEPS += \
./Kata20203315.d \
./helloThere.d 

OBJS += \
./Kata20203315.o \
./helloThere.o 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


clean: clean--2e-

clean--2e-:
	-$(RM) ./Kata20203315.d ./Kata20203315.o ./helloThere.d ./helloThere.o

.PHONY: clean--2e-

